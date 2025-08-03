#!/usr/bin/env python3
"""
Enhanced Sample Data Generator for Software Scorecard Dashboard v2
Creates realistic sample data including admin users, products, and comprehensive scorecards
"""

import asyncio
import aiohttp
import json
from datetime import datetime, date, timedelta
import random

BASE_URL = "http://localhost:8000"

# Sample data configurations
ADMIN_USERS = [
    {"email": "admin@company.com", "password": "admin123"},
    {"email": "manager@company.com", "password": "manager123"},
]

PRODUCTS = [
    {"name": "E-Commerce Platform", "description": "Main customer-facing e-commerce application"},
    {"name": "Payment Gateway", "description": "Secure payment processing service"},
    {"name": "User Management API", "description": "Authentication and user management microservice"},
    {"name": "Analytics Dashboard", "description": "Business intelligence and analytics platform"},
    {"name": "Mobile App Backend", "description": "API backend for mobile applications"},
]

# Security scorecard field configurations with realistic distributions
SECURITY_FIELDS = {
    # Static & Dynamic Testing
    "sast": 0.7,  # 70% have SAST
    "dast": 0.5,  # 50% have DAST
    "sast_dast_in_ci": 0.4,  # 40% integrate in CI/CD
    "triaging_findings": 0.6,  # 60% triage findings
    # Tooling & Integration
    "secrets_scanning": 0.3,  # 30% scan secrets
    "sca_tool_used": 0.4,  # 40% use SCA tools
    "cve_alerts": 0.5,  # 50% have CVE alerts
    "security_tools": 0.6,  # 60% use professional tools
    # Policies & Practices
    "threat_modeling": 0.3,  # 30% do threat modeling
    "compliance": 0.4,  # 40% are compliant
    "training": 0.2,  # 20% provide security training
    "bug_bounty_policy": 0.1,  # 10% have bug bounty
    "owasp_samm_integration": 0.2,  # 20% use OWASP SAMM
}

AUTOMATION_FIELDS = {
    # Test Automation Framework
    "automated_testing": 0.8,  # 80% have some automation
    "dedicated_environment": 0.6,  # 60% have dedicated env
    "testing_framework": 0.7,  # 70% have framework
    "external_updates": 0.4,  # 40% stay current
    "quick_setup": 0.5,  # 50% can setup quickly
    "source_controlled": 0.9,  # 90% use source control
    "seeded_data": 0.7,  # 70% use seeded data
    "test_independence": 0.8,  # 80% have independent tests
    "data_reseeding": 0.6,  # 60% can re-seed easily
    "test_subsets": 0.5,  # 50% can run subsets
    "rapid_updates": 0.4,  # 40% update tests quickly
    "database_automation": 0.5,  # 50% automate DB connections
    "post_deploy_sanity": 0.6,  # 60% have post-deploy tests
    "sanity_independence": 0.7,  # 70% have independent sanity tests
    "smoke_testing": 0.8,  # 80% have smoke tests
    "test_reporting": 0.7,  # 70% have reporting
    "notification_integration": 0.4,  # 40% have notifications
}

PERFORMANCE_FIELDS = {
    # Performance Strategy & Tooling
    "regular_testing": 0.4,  # 40% test regularly
    "dedicated_tools": 0.3,  # 30% use dedicated tools
    "ci_integration": 0.2,  # 20% integrate in CI/CD
    "defined_thresholds": 0.5,  # 50% have thresholds
    "trend_tracking": 0.3,  # 30% track trends
    # Test Coverage & Types
    "production_like_env": 0.4,  # 40% test in prod-like env
    # Metrics & Observability
    "latency_throughput": 0.6,  # 60% measure basic metrics
    "error_saturation": 0.4,  # 40% monitor error/saturation
    "dashboard_viz": 0.3,  # 30% have dashboards
    "automated_alerting": 0.4,  # 40% have alerting
    "monitoring_integration": 0.2,  # 20% have full integration
}

CICD_FIELDS = {
    # Pipeline Maturity
    "automated_builds": 0.8,  # 80% have automated builds
    "automated_tests": 0.7,  # 70% have automated tests
    "automated_deployment": 0.5,  # 50% have automated deployment
    "rollback_capability": 0.4,  # 40% have rollback
    "blue_green_deployment": 0.2,  # 20% use blue-green
    "canary_releases": 0.1,  # 10% use canary
    "infrastructure_as_code": 0.3,  # 30% use IaC
}

FIELD_CONFIGS = {
    "security": SECURITY_FIELDS,
    "automation": AUTOMATION_FIELDS,
    "performance": PERFORMANCE_FIELDS,
    "cicd": CICD_FIELDS,
}


async def create_admin_user(session, user_data):
    """Create an admin user"""
    try:
        async with session.post(f"{BASE_URL}/auth/register", json=user_data) as response:
            if response.status == 200:
                print(f"✅ Created admin user: {user_data['email']}")
                return True
            else:
                error_text = await response.text()
                print(f"❌ Failed to create user {user_data['email']}: {error_text}")
                return False
    except Exception as e:
        print(f"❌ Error creating user {user_data['email']}: {e}")
        return False


async def login_user(session, email, password):
    """Login and get access token"""
    try:
        async with session.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password}) as response:
            if response.status == 200:
                data = await response.json()
                token = data["access_token"]
                print(f"✅ Logged in as: {email}")
                return token
            else:
                print(f"❌ Failed to login: {email}")
                return None
    except Exception as e:
        print(f"❌ Login error for {email}: {e}")
        return None


async def create_product(session, token, product_data):
    """Create a product"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with session.post(f"{BASE_URL}/products", json=product_data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Created product: {product_data['name']}")
                return data["id"]
            else:
                error_text = await response.text()
                print(f"❌ Failed to create product {product_data['name']}: {error_text}")
                return None
    except Exception as e:
        print(f"❌ Error creating product {product_data['name']}: {e}")
        return None


def generate_realistic_scorecard(category, base_date, variation=0.1):
    """Generate realistic scorecard data with some randomness"""
    fields = FIELD_CONFIGS[category]
    breakdown = {}
    
    for field, base_probability in fields.items():
        # Add some randomness to make it realistic
        probability = max(0, min(1, base_probability + random.uniform(-variation, variation)))
        breakdown[field] = random.random() < probability
    
    # Add special handling for non-boolean fields
    if category == "automation":
        # API Coverage
        coverage_options = ["0%", "1-20%", "20-40%", "40-60%", "60-80%", "80-100%"]
        breakdown["api_coverage"] = random.choice(coverage_options)
        
        # Functional Coverage
        func_coverage_options = ["0%", "1-20%", "20-40%", "40-100%"]
        breakdown["functional_coverage"] = random.choice(func_coverage_options)
    
    elif category == "performance":
        # Test Types
        test_types = ["smoke", "load", "stress", "spike", "soak"]
        breakdown["test_types"] = random.choice(test_types)
        
        # Workflow Coverage
        workflow_options = ["0%", "1-20%", "20-50%", "50-100%"]
        breakdown["workflow_coverage"] = random.choice(workflow_options)
    
    elif category == "cicd":
        # DORA Metrics
        deployment_freq_options = ["monthly", "weekly", "daily", "on-demand"]
        breakdown["deployment_frequency"] = random.choice(deployment_freq_options)
        
        lead_time_options = [">1week", "<1week", "<1day", "<1hour"]
        breakdown["lead_time"] = random.choice(lead_time_options)
        
        recovery_time_options = [">1week", "<1week", "<1day", "<1hour"]
        breakdown["recovery_time"] = random.choice(recovery_time_options)
        
        failure_rate_options = [">45%", "31-45%", "16-30%", "0-15%"]
        breakdown["change_failure_rate"] = random.choice(failure_rate_options)
    
    return breakdown


async def create_scorecard(session, token, product_id, category, date_str, breakdown):
    """Create a scorecard"""
    headers = {"Authorization": f"Bearer {token}"}
    scorecard_data = {
        "product_id": product_id,
        "category": category,
        "date": date_str,
        "breakdown": breakdown
    }
    
    try:
        async with session.post(f"{BASE_URL}/scorecards", json=scorecard_data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Created {category} scorecard for product {product_id} (Score: {data['score']:.1f}%)")
                return data
            else:
                error_text = await response.text()
                print(f"❌ Failed to create scorecard: {error_text}")
                return None
    except Exception as e:
        print(f"❌ Error creating scorecard: {e}")
        return None


async def generate_historical_data(session, token, product_ids):
    """Generate quarterly scorecard data for the past 2 years"""
    categories = ["security", "automation", "performance", "cicd"]
    end_date = date.today()
    
    # Generate quarterly data for past 8 quarters (2 years)
    quarters = []
    current_year = end_date.year
    current_quarter = ((end_date.month - 1) // 3) + 1
    
    # Generate 8 quarters of data
    for i in range(8):
        quarter = current_quarter - i
        year = current_year
        
        if quarter <= 0:
            quarter += 4
            year -= 1
        
        # Set date to middle of quarter
        quarter_months = {1: 2, 2: 5, 3: 8, 4: 11}  # Feb, May, Aug, Nov
        quarter_date = date(year, quarter_months[quarter], 15)
        
        # Skip future dates
        if quarter_date <= end_date:
            quarters.append((quarter_date, f"{year}-Q{quarter}"))
    
    print(f"\n📊 Generating quarterly data for {len(quarters)} quarters...")
    
    for quarter_date, quarter_label in reversed(quarters):  # Oldest first
        date_str = quarter_date.isoformat()
        
        for product_id in product_ids:
            for category in categories:
                # Add improvement over time (older quarters tend to have lower scores)
                quarters_back = len(quarters) - quarters.index((quarter_date, quarter_label)) - 1
                improvement_factor = quarters_back / 8.0 * 0.3  # Up to 30% improvement over 2 years
                
                breakdown = generate_realistic_scorecard(
                    category, 
                    quarter_date, 
                    variation=0.1 + (improvement_factor * 0.5)
                )
                
                await create_scorecard(session, token, product_id, category, date_str, breakdown)
                print(f"  📈 {quarter_label} {category.capitalize()} scorecard for Product {product_id}")
                
                # Small delay to avoid overwhelming the server
                await asyncio.sleep(0.1)


async def main():
    """Main function to generate all sample data"""
    print("🚀 Starting Software Scorecard Dashboard v2 Sample Data Generation")
    print("=" * 70)
    
    async with aiohttp.ClientSession() as session:
        # Step 1: Create admin users
        print("\n📝 Creating Admin Users...")
        for user_data in ADMIN_USERS:
            await create_admin_user(session, user_data)
        
        # Step 2: Login with first admin user
        print("\n🔐 Logging in...")
        token = await login_user(session, ADMIN_USERS[0]["email"], ADMIN_USERS[0]["password"])
        
        if not token:
            print("❌ Failed to login. Aborting data generation.")
            return
        
        # Step 3: Create products
        print("\n🏗️ Creating Products...")
        product_ids = []
        for product_data in PRODUCTS:
            product_id = await create_product(session, token, product_data)
            if product_id:
                product_ids.append(product_id)
        
        if not product_ids:
            print("❌ No products created. Aborting scorecard generation.")
            return
        
        # Step 4: Generate current scorecards
        print("\n📊 Creating Current Scorecards...")
        categories = ["security", "automation", "performance", "cicd"]
        today = date.today().isoformat()
        
        for product_id in product_ids:
            for category in categories:
                breakdown = generate_realistic_scorecard(category, date.today())
                await create_scorecard(session, token, product_id, category, today, breakdown)
        
        # Step 5: Generate historical data
        print("\n📈 Generating Historical Trend Data (90 days)...")
        await generate_historical_data(session, token, product_ids)
        
        print("\n" + "=" * 70)
        print("✅ Sample data generation complete!")
        print("\n🎯 Summary:")
        print(f"   • Admin Users: {len(ADMIN_USERS)}")
        print(f"   • Products: {len(product_ids)}")
        print(f"   • Categories: {len(categories)}")
        print(f"   • Historical Data: ~90 days")
        print("\n🔑 Login Credentials:")
        for user in ADMIN_USERS:
            print(f"   • Email: {user['email']}, Password: {user['password']}")
        print("\n🌐 Access the dashboard at: http://localhost:3000 (or your frontend URL)")


if __name__ == "__main__":
    asyncio.run(main())
