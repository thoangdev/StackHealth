#!/bin/bash

# StackHealth Development Environment Setup
echo "🚀 Setting up StackHealth development environment..."

# Check if Python 3.9+ is installed
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
required_version="3.9"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" 2>/dev/null; then
    echo "❌ Python 3.9+ required. Current version: $(python3 --version)"
    exit 1
fi

echo "✅ Python version check passed"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install production dependencies
echo "📋 Installing production dependencies..."
pip install -r backend/requirements.txt

# Install development dependencies
echo "🛠️ Installing development dependencies..."
pip install -r backend/requirements-dev.txt

# Install pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install

# Copy environment configuration if it doesn't exist
if [ ! -f "config/.env.development" ]; then
    echo "⚙️ Creating development configuration..."
    cp config/.env.example config/.env.development
    echo "📝 Please edit config/.env.development with your settings"
else
    echo "✅ Development configuration already exists"
fi

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir -p data
else
    echo "✅ Data directory already exists"
fi

# Initialize database (optional)
echo "🗄️ Initializing database..."
cd backend
python -c "
try:
    from database import engine, Base
    Base.metadata.create_all(bind=engine)
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'⚠️ Database initialization skipped: {e}')
"
cd ..

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
cd backend
if pytest --version > /dev/null 2>&1; then
    pytest -v --tb=short
    if [ $? -eq 0 ]; then
        echo "✅ All tests passed!"
    else
        echo "⚠️ Some tests failed. Check the output above."
    fi
else
    echo "⚠️ pytest not available. Skipping test verification."
fi
cd ..

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Start the backend: cd backend && python main.py"
echo "3. Open frontend: open frontend/index.html"
echo "4. Run tests: cd backend && pytest"
echo "5. Format code: black backend && isort backend"
echo ""
echo "Happy coding! 🚀"
