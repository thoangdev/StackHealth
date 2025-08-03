#!/bin/bash

# Software Scorecard Dashboard v2 - Enhanced Setup Script
echo "🚀 Setting up Software Scorecard Dashboard v2..."
echo "================================================"

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Start the backend: ./scripts/start_backend.sh"
echo "2. Open frontend/index_new.html in your browser"
echo "3. Generate sample data: python scripts/create_enhanced_sample_data.py"
echo ""
echo "🔑 Default admin credentials will be created:"
echo "   Email: admin@company.com"
echo "   Password: admin123"
echo ""
echo "🐳 Alternative: Run with Docker using: ./scripts/docker-start.sh"
