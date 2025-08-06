#!/usr/bin/env python3
"""
Simple script to generate Postman collection using only standard library.
Used by GitHub Actions workflow.
"""

import json
import urllib.request
import urllib.error
import sys
from datetime import datetime


def fetch_openapi_spec(base_url):
    """Fetch OpenAPI spec using urllib"""
    try:
        with urllib.request.urlopen(f"{base_url}/openapi.json", timeout=10) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"❌ Error fetching OpenAPI spec: {e}")
        return None


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
                "value": "http://localhost:8000",
                "type": "string"
            },
            {
                "key": "authToken",
                "value": "",
                "type": "string",
                "description": "Bearer token from /auth/login"
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
                        "header": [
                            {
                                "key": "Content-Type",
                                "value": "application/json",
                                "type": "text"
                            }
                        ],
                        "url": {
                            "raw": "{{baseUrl}}" + path,
                            "host": ["{{baseUrl}}"],
                            "path": [p for p in path.split("/") if p]
                        },
                        "description": details.get("description", "")
                    }
                }
                
                # Add authentication for protected endpoints
                needs_auth = not (path in ["/", "/health", "/health/detailed", "/health/readiness", "/health/liveness"])
                
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
                
                # Add query parameters
                if "parameters" in details:
                    query_params = []
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
                
                # Add simple request body for POST/PUT requests
                if method.upper() in ["POST", "PUT", "PATCH"] and "requestBody" in details:
                    # Create a simple example based on the endpoint
                    if "/auth/login" in path:
                        example = {"email": "user@example.com", "password": "password"}
                    elif "/auth/register" in path:
                        example = {"email": "user@example.com", "password": "password"}
                    elif "/products" in path:
                        example = {"name": "Example Product", "description": "Product description"}
                    elif "/scorecards" in path:
                        example = {
                            "product_id": 1,
                            "category": "automation",
                            "date": "2024-01-01",
                            "breakdown": {}
                        }
                    else:
                        example = {}
                    
                    request_item["request"]["body"] = {
                        "mode": "raw",
                        "raw": json.dumps(example, indent=2),
                        "options": {
                            "raw": {
                                "language": "json"
                            }
                        }
                    }
                
                grouped_endpoints[tag].append(request_item)
    
    # Convert grouped endpoints to collection items
    tag_order = ["health", "auth", "products", "scorecards", "analytics"]
    
    for tag in tag_order:
        if tag in grouped_endpoints:
            folder = {
                "name": tag.title().replace("Auth", "Authentication"),
                "item": grouped_endpoints[tag]
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


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"🌐 Fetching OpenAPI spec from {base_url}")
    openapi_spec = fetch_openapi_spec(base_url)
    
    if not openapi_spec:
        print("❌ Failed to get OpenAPI specification")
        sys.exit(1)
    
    print("🔄 Converting to Postman collection...")
    postman_collection = convert_openapi_to_postman(openapi_spec, base_url)
    
    # Write Postman collection
    with open("stackhealth-api-collection.json", "w") as f:
        json.dump(postman_collection, f, indent=2)
    
    # Write OpenAPI spec
    with open("openapi.json", "w") as f:
        json.dump(openapi_spec, f, indent=2)
    
    print("✅ Postman collection generated successfully!")
    print(f"📁 Collection name: {postman_collection['info']['name']}")
    print(f"📊 Total folders: {len(postman_collection['item'])}")
    total_requests = sum(len(folder['item']) for folder in postman_collection['item'])
    print(f"🔗 Total requests: {total_requests}")


if __name__ == "__main__":
    main()
