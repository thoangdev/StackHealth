#!/bin/bash

# Docker Stop Script for Software Scorecard Dashboard

echo "🛑 Stopping Software Scorecard Dashboard Docker containers..."
echo "============================================================"

# Navigate to project root
cd ..

# Stop and remove containers
docker-compose down

echo ""
echo "✅ Containers stopped successfully!"
echo ""
echo "💡 To completely remove images and volumes:"
echo "   docker-compose down --rmi all --volumes"
