#!/bin/bash

# Software Scorecard Dashboard - Start Script
# This script starts the FastAPI backend server

echo "🎯 Starting Software Scorecard Dashboard Backend..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment and start server
source ../.venv/bin/activate

echo "🚀 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📖 ReDoc Documentation: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

cd ../backend && python main.py
