# Using the StackHealth API Collection

This guide shows how to use the automatically generated Postman collection for the StackHealth API.

## Quick Start

### 1. Import the Collection

1. Download `stackhealth-api-collection.json` from the latest GitHub Actions run or generate it locally
2. Open Postman
3. Click **Import** → **Files** → Select the JSON file
4. The collection will appear in your workspace

### 2. Set Up Environment

Create a new environment or use variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `baseUrl` | `http://localhost:8000` | Your API server URL |
| `authToken` | (empty initially) | Bearer token from login |

### 3. Authentication Workflow

1. **Register a User** (if needed)
   - Use `POST /auth/register` in the Authentication folder
   - Provide email and password

2. **Login**
   - Use `POST /auth/login`
   - Enter your email and password
   - Copy the `access_token` from the response

3. **Set Auth Token**
   - Paste the token into the `authToken` environment variable
   - All authenticated endpoints will now work automatically

### 4. Test the API

Try these endpoints in order:

1. **Health Check**
   ```
   GET /health
   ```

2. **Create a Product**
   ```
   POST /products
   {
     "name": "My Test Product",
     "description": "A product for testing"
   }
   ```

3. **Submit a Scorecard**
   ```
   POST /scorecards
   {
     "product_id": 1,
     "category": "automation",
     "date": "2024-01-01",
     "breakdown": {
       "automated_testing": true,
       "dedicated_environment": true,
       "testing_framework": true
     }
   }
   ```

4. **View Scorecards**
   ```
   GET /scorecards
   ```

## Example Scorecard Data

### Automation Scorecard
```json
{
  "product_id": 1,
  "category": "automation",
  "date": "2024-01-01",
  "breakdown": {
    "automated_testing": true,
    "dedicated_environment": true,
    "testing_framework": true,
    "external_updates": false,
    "quick_setup": true,
    "source_controlled": true,
    "seeded_data": true,
    "test_independence": true,
    "data_reseeding": true,
    "test_subsets": true,
    "rapid_updates": false,
    "database_automation": true,
    "post_deploy_sanity": true,
    "sanity_independence": true,
    "smoke_testing": true,
    "test_reporting": true,
    "notification_integration": true,
    "api_coverage": "60-80%",
    "functional_coverage": "40-100%"
  }
}
```

### Security Scorecard
```json
{
  "product_id": 1,
  "category": "security",
  "date": "2024-01-01",
  "breakdown": {
    "sast": true,
    "dast": true,
    "sast_dast_in_ci": true,
    "triaging_findings": true,
    "secrets_scanning": true,
    "sca_tool_used": true,
    "cve_alerts": true,
    "security_tools": true,
    "threat_modeling": true,
    "compliance": true,
    "training": true,
    "bug_bounty_policy": false,
    "owasp_samm_integration": true
  }
}
```

### Performance Scorecard
```json
{
  "product_id": 1,
  "category": "performance",
  "date": "2024-01-01",
  "breakdown": {
    "regular_testing": true,
    "dedicated_tools": true,
    "ci_integration": true,
    "defined_thresholds": true,
    "trend_tracking": true,
    "test_types": "load,stress,spike",
    "production_like_env": true,
    "workflow_coverage": "50-100%",
    "latency_throughput": true,
    "error_saturation": true,
    "dashboard_viz": true,
    "automated_alerting": true,
    "monitoring_integration": true
  }
}
```

### CI/CD Scorecard
```json
{
  "product_id": 1,
  "category": "cicd",
  "date": "2024-01-01",
  "breakdown": {
    "deployment_frequency": "daily",
    "lead_time": "<1day",
    "recovery_time": "<1hour",
    "change_failure_rate": "0-15%",
    "automated_builds": true,
    "automated_tests": true,
    "automated_deployment": true,
    "rollback_capability": true,
    "blue_green_deployment": false,
    "canary_releases": false,
    "infrastructure_as_code": true
  }
}
```

## Testing Workflows

### 1. Complete Product Lifecycle
1. Create product
2. Submit scorecards for all categories
3. View aggregated scorecards
4. Generate PDF reports
5. Check trend data

### 2. User Management (Admin)
1. Register users
2. Login as admin
3. Manage admin privileges
4. View all users

### 3. Analytics
1. Submit multiple scorecards over time
2. View trend data
3. Check quarterly improvements

## Troubleshooting

### Authentication Errors
- Ensure `authToken` is set correctly
- Check token hasn't expired (re-login if needed)
- Verify you're using Bearer format

### Validation Errors
- Check required fields in request body
- Verify data types (dates, numbers, booleans)
- Ensure valid category names

### 404 Errors
- Verify product exists before creating scorecards
- Check endpoint URLs are correct
- Ensure server is running

## Advanced Usage

### Automation Testing
Use the collection with Newman (Postman CLI) for automated testing:

```bash
npm install -g newman
newman run stackhealth-api-collection.json \
  --environment your-environment.json \
  --reporters cli,json
```

### CI/CD Integration
Include API tests in your pipeline:

```yaml
- name: Test API
  run: |
    newman run api-spec/stackhealth-api-collection.json \
      --env-var baseUrl=http://localhost:8000 \
      --env-var authToken=${{ secrets.API_TOKEN }}
```

## Collection Updates

The collection is automatically updated on every push to main. To get the latest version:

1. Check the GitHub Actions artifacts
2. Download the new collection
3. Re-import to Postman (it will update existing requests)

Or generate locally:
```bash
make dev  # Start the server
make api-spec  # Generate collection
```
