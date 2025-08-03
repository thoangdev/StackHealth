#!/usr/bin/env python3
"""
Sample data generator for Software Scorecard Dashboard
This script creates sample projects and scorecards for testing
"""

import requests
import json
from datetime import date, timedelta
import random
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_BASE_URL = "http://localhost:8000"

def create_sample_data():
    """Create sample projects and scorecards"""
    
    print("🎯 Creating sample data for Software Scorecard Dashboard...")
    
    # Sample projects
    projects = [
        {
            "name": "E-Commerce Platform",
            "description": "Main customer-facing e-commerce application"
        },
        {
            "name": "Mobile App Backend",
            "description": "REST API backend for mobile applications"
        },
        {
            "name": "Analytics Dashboard",
            "description": "Internal analytics and reporting system"
        },
        {
            "name": "Payment Service",
            "description": "Microservice handling payment processing"
        }
    ]
    
    created_projects = []
    
    # Create projects
    print("\n📂 Creating sample projects...")
    for project in projects:
        try:
            response = requests.post(f"{API_BASE_URL}/projects", json=project)
            if response.status_code == 200:
                created_project = response.json()
                created_projects.append(created_project)
                print(f"✅ Created project: {project['name']}")
            else:
                print(f"❌ Failed to create project: {project['name']} - {response.text}")
        except Exception as e:
            print(f"❌ Error creating project {project['name']}: {e}")
    
    # Create sample scorecards
    print("\n📊 Creating sample scorecards...")
    
    # Generate scorecards for the last 30 days
    for project in created_projects:
        for i in range(6):  # 6 scorecards per project over time
            scorecard_date = date.today() - timedelta(days=i*5)
            
            # Generate realistic scores with some variation
            base_scores = {
                "automation": random.randint(60, 95),
                "performance": random.randint(55, 90),
                "security": random.randint(70, 95),
                "cicd": random.randint(65, 90)
            }
            
            feedback = []
            
            # Add feedback for lower scores
            for area, score in base_scores.items():
                if score < 75 or random.random() < 0.3:  # 30% chance of feedback even for good scores
                    comments = {
                        "automation": [
                            "Need to increase test coverage",
                            "Manual testing still required for some features",
                            "UI tests are flaky and need improvement"
                        ],
                        "performance": [
                            "Database queries need optimization",
                            "API response times are slower than expected",
                            "Memory usage spikes during peak hours"
                        ],
                        "security": [
                            "Dependency vulnerabilities found",
                            "Authentication mechanisms need review",
                            "Security scanning should be automated"
                        ],
                        "cicd": [
                            "Build times are too long",
                            "Deployment process needs automation",
                            "Testing pipeline needs improvement"
                        ]
                    }
                    
                    tools = {
                        "automation": "Playwright, Cypress, Selenium",
                        "performance": "k6, JMeter, New Relic",
                        "security": "OWASP ZAP, Snyk, SonarQube",
                        "cicd": "GitHub Actions, Jenkins, GitLab CI"
                    }
                    
                    feedback.append({
                        "area": area,
                        "comment": random.choice(comments[area]),
                        "tool_recommendation": tools[area],
                        "marked_for_improvement": score < 70
                    })
            
            scorecard_data = {
                "project_id": project["id"],
                "date": scorecard_date.isoformat(),
                "automation_score": base_scores["automation"],
                "performance_score": base_scores["performance"],
                "security_score": base_scores["security"],
                "cicd_score": base_scores["cicd"],
                "feedback": feedback
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/scorecards", json=scorecard_data)
                if response.status_code == 200:
                    print(f"✅ Created scorecard for {project['name']} on {scorecard_date}")
                else:
                    print(f"❌ Failed to create scorecard for {project['name']}: {response.text}")
            except Exception as e:
                print(f"❌ Error creating scorecard for {project['name']}: {e}")
    
    print("\n🎉 Sample data creation complete!")
    print(f"📊 Visit http://localhost:8000/docs to explore the API")
    print(f"🌐 Open index.html in your browser to use the dashboard")

if __name__ == "__main__":
    try:
        # Test if API is running
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            create_sample_data()
        else:
            print("❌ API is not responding. Please start the backend server first.")
    except Exception as e:
        print(f"❌ Cannot connect to API at {API_BASE_URL}")
        print("Please make sure the backend server is running with: python main.py")
