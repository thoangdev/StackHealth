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
    "sast": 0.7,  # 70% of companies have SAST
    "dast": 0.5,  # 50% have DAST
    "sast_dast_in_ci": 0.4,  # 40% integrate security in CI/CD
    "triaging_findings": 0.6,  # 60% triage findings
    "secrets_scanning": 0.3,  # 30% scan secrets
    "sca_tool_used": 0.4,  # 40% use SCA tools
    "cve_alerts": 0.5,  # 50% have CVE alerts
    "pr_enforcement": 0.3,  # 30% enforce in PRs
    "training": 0.2,  # 20% provide security training
    "threat_modeling": 0.3,  # 30% do threat modeling
    "bug_bounty_policy": 0.1,  # 10% have bug bounty
    "compliance": 0.4,  # 40% are compliant
    "secure_design_reviews": 0.3,  # 30% do secure design reviews
    "predeployment_threat_modeling": 0.2,  # 20% do pre-deployment threat modeling
}

AUTOMATION_FIELDS = {
    "ci_pipeline": 0.8,  # 80% have CI
    "automated_testing": 0.6,  # 60% have automated testing
    "deployment_automation": 0.5,  # 50% have automated deployment
    "monitoring_alerts": 0.7,  # 70% have monitoring
    "infrastructure_as_code": 0.4,  # 40% use IaC
}

PERFORMANCE_FIELDS = {
    "load_testing": 0.4,  # 40% do load testing
    "performance_monitoring": 0.6,  # 60% have performance monitoring
    "caching_strategy": 0.5,  # 50% have caching
    "database_optimization": 0.3,  # 30% optimize databases
    "cdn_usage": 0.7,  # 70% use CDN
}

CICD_FIELDS = {
    "automated_builds": 0.8,  # 80% have automated builds
    "automated_tests": 0.6,  # 60% run automated tests in pipeline
    "code_quality_gates": 0.4,  # 40% have quality gates
    "deployment_pipeline": 0.5,  # 50% have deployment pipelines
    "rollback_strategy": 0.3,  # 30% have rollback strategy
    "environment_parity": 0.4,  # 40% have environment parity
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
    """Generate historical scorecard data for the past 90 days"""
    categories = ["security", "automation", "performance", "cicd"]
    end_date = date.today()
    
    # Generate data for past 90 days with weekly intervals
    for days_back in range(0, 91, 7):  # Every 7 days
        scorecard_date = end_date - timedelta(days=days_back)
        date_str = scorecard_date.isoformat()
        
        for product_id in product_ids:
            for category in categories:
                # Add some improvement over time (older data tends to be worse)
                improvement_factor = days_back / 90.0 * 0.2  # Up to 20% worse for older data
                breakdown = generate_realistic_scorecard(category, scorecard_date, variation=0.1 + improvement_factor)
                
                await create_scorecard(session, token, product_id, category, date_str, breakdown)
                
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
