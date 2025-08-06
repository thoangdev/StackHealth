#!/usr/bin/env python3
"""
Generate Postman collection from FastAPI OpenAPI specification.
Can be run locally or in CI/CD pipeline.

Usage:
    python scripts/generate_postman_collection.py
    python scripts/generate_postman_collection.py --url http://localhost:8000
"""

import json
import argparse
import httpx
import sys
from datetime import datetime
from pathlib import Path


def convert_openapi_to_postman(openapi_spec, base_url="{{baseUrl}}"):
    """Convert OpenAPI spec to Postman collection format"""
    
    collection = {
        "info": {
            "name": openapi_spec.get("info", {}).get("title", "StackHealth API"),
            "description": openapi_spec.get("info", {}).get("description", ""),
            "version": openapi_spec.get("info", {}).get("version", "1.0.0"),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [],
        "variable": [
            {
                "key": "baseUrl",
                "value": base_url.replace("{{baseUrl}}", "http://localhost:8000"),
                "type": "string"
            },
            {
                "key": "authToken",
                "value": "",
                "type": "string",
                "description": "Bearer token obtained from /auth/login"
            }
        ],
        "auth": {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{authToken}}",
                    "type": "string"
                }
            ]
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "// Auto-set content-type for JSON requests",
                        "if (pm.request.body && pm.request.body.mode === 'raw') {",
                        "    pm.request.headers.add({",
                        "        key: 'Content-Type',",
                        "        value: 'application/json'",
                        "    });",
                        "}"
                    ]
                }
            }
        ]
    }
    
    # Group endpoints by tags
    grouped_endpoints = {}
    
    for path, methods in openapi_spec.get("paths", {}).items():
        for method, details in methods.items():
            if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                tags = details.get("tags", ["Untagged"])
                tag = tags[0] if tags else "Untagged"
                
                if tag not in grouped_endpoints:
                    grouped_endpoints[tag] = []
                    
                # Create request object
                request_item = {
                    "name": details.get("summary", f"{method.upper()} {path}"),
                    "request": {
                        "method": method.upper(),
                        "header": [],
                        "url": {
                            "raw": "{{baseUrl}}" + path,
                            "host": ["{{baseUrl}}"],
                            "path": [p for p in path.split("/") if p]
                        },
                        "description": details.get("description", "")
                    },
                    "response": []
                }
                
                # Add authentication for protected endpoints (most endpoints except health and root)
                needs_auth = not (path in ["/", "/health", "/health/detailed", "/health/readiness", "/health/liveness"] 
                                or path.startswith("/openapi") or path.startswith("/docs"))
                
                if needs_auth:
                    request_item["request"]["auth"] = {
                        "type": "bearer",
                        "bearer": [
                            {
                                "key": "token",
                                "value": "{{authToken}}",
                                "type": "string"
                            }
                        ]
                    }
                
                # Add path parameters
                path_params = []
                if "parameters" in details:
                    for param in details["parameters"]:
                        if param.get("in") == "path":
                            # Replace path parameter in URL
                            param_name = param["name"]
                            request_item["request"]["url"]["raw"] = request_item["request"]["url"]["raw"].replace(
                                f"{{{param_name}}}", f":{param_name}"
                            )
                            path_params.append({
                                "key": param_name,
                                "value": "",
                                "description": param.get("description", "")
                            })
                
                if path_params:
                    request_item["request"]["url"]["variable"] = path_params
                
                # Add query parameters
                query_params = []
                if "parameters" in details:
                    for param in details["parameters"]:
                        if param.get("in") == "query":
                            query_params.append({
                                "key": param["name"],
                                "value": "",
                                "description": param.get("description", ""),
                                "disabled": not param.get("required", False)
                            })
                
                if query_params:
                    request_item["request"]["url"]["query"] = query_params
                
                # Add request body for POST/PUT requests
                if method.upper() in ["POST", "PUT", "PATCH"] and "requestBody" in details:
                    content = details["requestBody"].get("content", {})
                    if "application/json" in content:
                        schema = content["application/json"].get("schema", {})
                        example = generate_example_from_schema(schema, openapi_spec.get("components", {}))
                        request_item["request"]["body"] = {
                            "mode": "raw",
                            "raw": json.dumps(example, indent=2),
                            "options": {
                                "raw": {
                                    "language": "json"
                                }
                            }
                        }
                
                # Add example responses
                if "responses" in details:
                    for status_code, response_details in details["responses"].items():
                        if status_code.startswith("2"):  # Success responses
                            content = response_details.get("content", {})
                            if "application/json" in content:
                                schema = content["application/json"].get("schema", {})
                                example_response = generate_example_from_schema(schema, openapi_spec.get("components", {}))
                                request_item["response"].append({
                                    "name": f"Success ({status_code})",
                                    "originalRequest": request_item["request"],
                                    "status": response_details.get("description", "Success"),
                                    "code": int(status_code),
                                    "header": [
                                        {
                                            "key": "Content-Type",
                                            "value": "application/json"
                                        }
                                    ],
                                    "body": json.dumps(example_response, indent=2)
                                })
                
                grouped_endpoints[tag].append(request_item)
    
    # Convert grouped endpoints to collection items with proper ordering
    tag_order = ["health", "auth", "products", "scorecards", "analytics"]
    
    # Add ordered folders first
    for tag in tag_order:
        if tag in grouped_endpoints:
            folder = {
                "name": tag.title().replace("Auth", "Authentication"),
                "item": grouped_endpoints[tag],
                "description": get_folder_description(tag)
            }
            collection["item"].append(folder)
    
    # Add remaining folders
    for tag, items in grouped_endpoints.items():
        if tag not in tag_order:
            folder = {
                "name": tag.title(),
                "item": items
            }
            collection["item"].append(folder)
    
    return collection


def get_folder_description(tag):
    """Get description for folder based on tag"""
    descriptions = {
        "health": "Health check endpoints for monitoring and diagnostics",
        "auth": "Authentication and user management endpoints",
        "products": "Product management endpoints",
        "scorecards": "Scorecard creation and retrieval endpoints",
        "analytics": "Analytics and trend data endpoints"
    }
    return descriptions.get(tag, "")


def generate_example_from_schema(schema, components):
    """Generate example data from JSON schema"""
    if "$ref" in schema:
        ref_path = schema["$ref"].replace("#/components/schemas/", "")
        if ref_path in components.get("schemas", {}):
            return generate_example_from_schema(components["schemas"][ref_path], components)
    
    schema_type = schema.get("type", "object")
    
    if schema_type == "object":
        example = {}
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        for prop_name, prop_schema in properties.items():
            if prop_name in required or prop_name in ["email", "password", "name", "product_id", "category", "date"]:
                example[prop_name] = generate_example_from_schema(prop_schema, components)
        
        # Add some common examples
        if "email" in example:
            example["email"] = "user@example.com"
        if "password" in example:
            example["password"] = "securepassword123"
        if "name" in example:
            example["name"] = "Example Product"
        if "category" in example:
            example["category"] = "automation"
        if "date" in example:
            example["date"] = "2024-01-01"
            
        return example
    elif schema_type == "array":
        items_schema = schema.get("items", {})
        return [generate_example_from_schema(items_schema, components)]
    elif schema_type == "string":
        if schema.get("format") == "email":
            return "user@example.com"
        elif schema.get("format") == "date":
            return "2024-01-01"
        elif schema.get("format") == "date-time":
            return "2024-01-01T00:00:00Z"
        elif "enum" in schema:
            return schema["enum"][0]
        else:
            return "string"
    elif schema_type == "integer":
        return 1
    elif schema_type == "number":
        return 1.0
    elif schema_type == "boolean":
        return True
    else:
        return None


def fetch_openapi_spec(base_url):
    """Fetch OpenAPI spec from running FastAPI server"""
    try:
        response = httpx.get(f"{base_url}/openapi.json", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching OpenAPI spec from {base_url}: {e}")
        return None


def generate_documentation(collection):
    """Generate markdown documentation from collection"""
    doc = f"""# {collection['info']['name']} - API Documentation

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Description
{collection['info']['description']}

## Version
{collection['info']['version']}

## Base URL
Configure the `baseUrl` variable in Postman with your API server URL (default: http://localhost:8000)

## Authentication
Most endpoints require authentication. Set the `authToken` variable with your Bearer token obtained from the login endpoint.

## Endpoints

"""
    
    for folder in collection['item']:
        doc += f"\n### {folder['name']}\n"
        if 'description' in folder:
            doc += f"{folder['description']}\n\n"
        
        for item in folder['item']:
            method = item['request']['method']
            url = item['request']['url']['raw'].replace('{{baseUrl}}', '')
            doc += f"- **{method}** `{url}` - {item['name']}\n"
    
    doc += f"""

## Import Instructions

### Postman
1. Download the `stackhealth-api-collection.json` file
2. Open Postman
3. Click **Import** button
4. Select the downloaded JSON file
5. Configure environment variables:
   - `baseUrl`: Your API server URL
   - `authToken`: Your authentication token

### Other Tools
The collection is compatible with other API clients that support Postman format, including:
- Insomnia
- Thunder Client (VS Code)
- API testing frameworks

## Getting Started
1. Import the collection
2. Set up environment variables
3. Call `POST /auth/login` to get an authentication token
4. Copy the token to the `authToken` variable
5. Start making authenticated requests

"""
    
    return doc


def main():
    parser = argparse.ArgumentParser(description="Generate Postman collection from FastAPI OpenAPI spec")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the FastAPI server")
    parser.add_argument("--output-dir", default="api-spec", help="Output directory for generated files")
    parser.add_argument("--local-spec", help="Path to local OpenAPI spec file (skip fetching)")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Get OpenAPI specification
    if args.local_spec:
        print(f"📁 Reading OpenAPI spec from {args.local_spec}")
        with open(args.local_spec, 'r') as f:
            openapi_spec = json.load(f)
    else:
        print(f"🌐 Fetching OpenAPI spec from {args.url}")
        openapi_spec = fetch_openapi_spec(args.url)
        
    if not openapi_spec:
        print("❌ Failed to get OpenAPI specification")
        sys.exit(1)
    
    # Convert to Postman collection
    print("🔄 Converting to Postman collection...")
    postman_collection = convert_openapi_to_postman(openapi_spec, args.url)
    
    # Write files
    collection_file = output_dir / "stackhealth-api-collection.json"
    openapi_file = output_dir / "openapi.json"
    docs_file = output_dir / "api-documentation.md"
    
    with open(collection_file, 'w') as f:
        json.dump(postman_collection, f, indent=2)
    
    with open(openapi_file, 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    documentation = generate_documentation(postman_collection)
    with open(docs_file, 'w') as f:
        f.write(documentation)
    
    # Print summary
    print("\n✅ API specification generated successfully!")
    print(f"📁 Collection: {collection_file}")
    print(f"📁 OpenAPI spec: {openapi_file}")
    print(f"📁 Documentation: {docs_file}")
    print(f"📊 Collection name: {postman_collection['info']['name']}")
    print(f"📊 Total folders: {len(postman_collection['item'])}")
    total_requests = sum(len(folder['item']) for folder in postman_collection['item'])
    print(f"🔗 Total requests: {total_requests}")
    
    print(f"\n🚀 To use with Postman:")
    print(f"1. Import {collection_file}")
    print(f"2. Set baseUrl variable to {args.url}")
    print(f"3. Get auth token from POST /auth/login")
    print(f"4. Set authToken variable with your Bearer token")


if __name__ == "__main__":
    main()
