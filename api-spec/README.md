# StackHealth API Specification

This directory contains automatically generated API specifications for the StackHealth application.

## Files

- `stackhealth-api-collection.json` - Postman collection ready for import
- `openapi.json` - OpenAPI 3.0 specification
- `api-documentation.md` - Human-readable API documentation

## How to Use

### Postman Collection

1. **Import Collection**
   - Download `stackhealth-api-collection.json`
   - Open Postman
   - Click "Import" button
   - Select the downloaded JSON file

2. **Configure Environment**
   - Set `baseUrl` variable to your API server URL
     - Local development: `http://localhost:8000`
     - Production: Your deployed API URL
   - Set `authToken` variable (leave empty initially)

3. **Authenticate**
   - Use the `POST /auth/login` endpoint in the Authentication folder
   - Copy the returned `access_token`
   - Paste it into the `authToken` environment variable
   - Now all authenticated endpoints will work automatically

### Other API Clients

The OpenAPI specification (`openapi.json`) can be used with:
- **Swagger UI** - For interactive documentation
- **Insomnia** - Import OpenAPI spec directly
- **Thunder Client** (VS Code) - Import collection
- **curl** - Generate commands from the spec

## API Overview

### Authentication Endpoints
- Login and get access token
- Register new users
- Manage admin privileges
- User information

### Product Management
- Create and list products
- Product-based scorecard organization

### Scorecard Management
- Submit scorecards for different categories:
  - **Automation** - Test automation frameworks and coverage
  - **Performance** - Performance testing and monitoring
  - **Security** - Security scanning and practices  
  - **CI/CD** - Pipeline maturity and DORA metrics
- Retrieve scorecards with filtering
- Generate PDF reports

### Analytics
- Trend data over time
- Quarterly improvement tracking
- Category-specific insights

### Health Checks
- Basic health status
- Detailed system metrics
- Kubernetes readiness/liveness probes

## Authentication

Most endpoints require Bearer token authentication:

```
Authorization: Bearer <your-access-token>
```

Get your token by calling:
```
POST /auth/login
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

## Scorecard Categories

Valid categories for scorecards:
- `automation` - Test automation and framework metrics
- `performance` - Performance testing and monitoring  
- `security` - Security scanning and practices
- `cicd` - CI/CD pipeline maturity and DORA metrics

## Automatic Updates

This specification is automatically updated whenever code is pushed to the main branch via GitHub Actions. The workflow:

1. Starts the FastAPI server
2. Fetches the OpenAPI specification
3. Converts it to Postman collection format
4. Commits updated files back to the repository

## Local Generation

You can also generate the API specification locally:

```bash
# Start your FastAPI server
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Generate specifications (in another terminal)
python scripts/generate_postman_collection.py --url http://localhost:8000

# Or use the simpler script
python scripts/generate_api_spec.py http://localhost:8000
```

## Troubleshooting

### Collection Not Working
1. Verify `baseUrl` is set correctly
2. Ensure you have a valid `authToken`
3. Check that the API server is running

### Authentication Issues
1. Try the login endpoint first
2. Copy the exact token value (no extra spaces)
3. Verify your email/password are correct

### Missing Endpoints
1. Check if the server is running the latest code
2. Regenerate the collection
3. Verify the endpoint exists in `/docs` (Swagger UI)

## Contributing

When adding new endpoints:
1. Ensure proper OpenAPI documentation in FastAPI
2. Use appropriate tags for grouping
3. The collection will be automatically regenerated on push to main

For more information, see the [API documentation](http://localhost:8000/docs) when running locally.
