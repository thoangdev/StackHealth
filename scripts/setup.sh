#!/bin/bash

# Software Scorecard Dashboard - Setup Script
# This script sets up the development environment

echo "🎯 Setting up Software Scorecard Dashboard"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "../.venv" ]; then
    echo "📦 Creating virtual environment..."
    cd .. && python3 -m venv .venv && cd scripts
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../.venv/bin/activate

# Install requirements
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r ../backend/requirements.txt

# Create data directory
mkdir -p ../data

echo ""
echo "✅ Setup complete!"
echo "🚀 To start the backend server, run: ./start_backend.sh"
echo "🌐 To open the frontend, open frontend/index.html in your browser"
echo "🐳 To run with Docker, use: docker-compose up"
echo ""
echo "📚 API Documentation will be available at: http://localhost:8000/docs"
