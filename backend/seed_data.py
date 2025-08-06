#!/usr/bin/env python3
"""
Data seeding script for StackHealth Scorecard Platform
This script creates initial admin user and sample products when the application starts
"""

import database
import auth
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """Seed the database with initial data"""
    logger.info("Starting database seeding...")
    
    # Create database tables if they don't exist
    database.Base.metadata.create_all(bind=database.engine)
    logger.info("Database tables created/verified")
    
    # Create database session
    db = Session(bind=database.engine)
    
    try:
        # Check if admin user already exists
        existing_admin = auth.get_user_by_email(db, "admin@company.com")
        if not existing_admin:
            # Create admin user
            admin_user = auth.create_admin_user(db, "admin@company.com", "admin123", is_admin=True)
            logger.info(f"Created admin user: {admin_user.email}")
        else:
            logger.info("Admin user already exists: admin@company.com")
        
        # Check if any products exist
        existing_products = db.query(database.Product).count()
        if existing_products == 0:
            # Create sample products
            sample_products = [
                {
                    "name": "Web Application Platform",
                    "description": "Main customer-facing web application with user authentication and core business logic"
                },
                {
                    "name": "Mobile API Gateway",
                    "description": "RESTful API gateway serving mobile applications with rate limiting and authentication"
                },
                {
                    "name": "Data Analytics Service",
                    "description": "Microservice for processing and analyzing customer data with real-time reporting"
                },
                {
                    "name": "Payment Processing System",
                    "description": "Secure payment processing service with fraud detection and compliance monitoring"
                }
            ]
            
            for product_data in sample_products:
                product = database.Product(
                    name=product_data["name"],
                    description=product_data["description"]
                )
                db.add(product)
            
            db.commit()
            logger.info(f"Created {len(sample_products)} sample products")
        else:
            logger.info(f"Products already exist in database ({existing_products} products)")
        
        # Create a regular test user if it doesn't exist
        existing_user = auth.get_user_by_email(db, "user@company.com")
        if not existing_user:
            regular_user = auth.create_admin_user(db, "user@company.com", "user123", is_admin=False)
            logger.info(f"Created regular user: {regular_user.email}")
        else:
            logger.info("Regular user already exists: user@company.com")
            
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during database seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
