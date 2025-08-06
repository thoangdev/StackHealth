#!/bin/bash
# Manual database seeding script for development
# Run this if you want to reset and reseed the database

echo "🌱 Starting manual database seeding..."

# Execute the seeding script inside the backend container
docker-compose exec backend python seed_data.py

echo "✅ Database seeding completed!"
echo ""
echo "📋 Default credentials:"
echo "  Admin: admin@company.com / admin123"
echo "  User:  user@company.com / user123"
echo ""
echo "🚀 Access the application at: http://localhost:3000"
