# StackHealth Development Commands

.PHONY: help setup test lint format clean dev build deploy health

# Default target
help:
	@echo "StackHealth Development Commands"
	@echo "================================"
	@echo "setup     - Set up development environment"
	@echo "test      - Run all tests with coverage"
	@echo "test-unit - Run unit tests only"
	@echo "test-int  - Run integration tests only"
	@echo "lint      - Run linting (flake8, mypy, bandit)"
	@echo "format    - Format code (black, isort)"
	@echo "clean     - Clean up temporary files"
	@echo "dev       - Start development server"
	@echo "build     - Build Docker image"
	@echo "deploy    - Deploy with Docker Compose"
	@echo "health    - Check application health"
	@echo "pre-commit- Run pre-commit hooks on all files"
	@echo "api-spec  - Generate API specification for Postman"
	@echo "test-workflow - Test the GitHub Actions workflow locally"
	@echo "test-security - Test security scanning tools locally"

# Development setup
setup:
	@echo "🚀 Setting up development environment..."
	./scripts/setup-dev.sh

# Testing
test:
	@echo "🧪 Running all tests with coverage..."
	cd backend && pytest --cov=. --cov-report=html --cov-report=term-missing -v

test-unit:
	@echo "🧪 Running unit tests..."
	cd backend && pytest -m "not integration" -v

test-int:
	@echo "🧪 Running integration tests..."
	cd backend && pytest -m integration -v

test-security:
	@echo "🔒 Running security tests..."
	cd backend && pytest -m security -v

# Code quality
lint:
	@echo "🔍 Running linting..."
	cd backend && flake8 .
	cd backend && mypy . --ignore-missing-imports
	cd backend && bandit -r . -f json -o ../reports/bandit-report.json || true

format:
	@echo "✨ Formatting code..."
	cd backend && black .
	cd backend && isort .
	@echo "✅ Code formatting complete!"

# Pre-commit
pre-commit:
	@echo "🪝 Running pre-commit hooks..."
	pre-commit run --all-files

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.coverage" -delete
	rm -rf backend/htmlcov/
	rm -rf backend/.pytest_cache/
	rm -rf backend/.mypy_cache/
	rm -rf reports/
	@echo "✅ Cleanup complete!"

# Development server
dev:
	@echo "🚀 Starting development server..."
	cd backend && python main.py --reload

# Docker operations
build:
	@echo "🐳 Building Docker image..."
	docker build -t stackhealth:latest .

deploy:
	@echo "🚀 Deploying with Docker Compose..."
	docker-compose up -d

deploy-dev:
	@echo "🚀 Starting development environment with Docker..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

stop:
	@echo "🛑 Stopping Docker services..."
	docker-compose down

# Health check
health:
	@echo "🏥 Checking application health..."
	curl -f http://localhost:8000/health || echo "❌ Backend not responding"
	@echo ""
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r backend/requirements.txt

install-dev:
	@echo "📦 Installing development dependencies..."
	pip install -r backend/requirements-dev.txt

# Database operations
db-init:
	@echo "🗄️ Initializing database..."
	cd backend && python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"

db-reset:
	@echo "🗄️ Resetting database..."
	rm -f data/scorecard.db
	$(MAKE) db-init

# Reports
reports:
	@echo "📊 Generating reports..."
	mkdir -p reports
	cd backend && pytest --cov=. --cov-report=html --cov-report=xml
	mv backend/htmlcov reports/
	mv backend/coverage.xml reports/
	@echo "📊 Reports generated in reports/ directory"

# API Specification
api-spec:
	@echo "📋 Generating API specification..."
	@if ! curl -f http://localhost:8000/health >/dev/null 2>&1; then \
		echo "❌ API server not running. Start it with 'make dev' first."; \
		exit 1; \
	fi
	python3 scripts/generate_api_spec.py http://localhost:8000
	@echo "✅ API specification generated in api-spec/ directory"
	@echo "📁 Files created:"
	@echo "   - stackhealth-api-collection.json (Postman collection)"
	@echo "   - openapi.json (OpenAPI specification)"
	@echo "💡 Import the Postman collection to test your API!"

api-spec-advanced:
	@echo "📋 Generating advanced API specification..."
	@if ! curl -f http://localhost:8000/health >/dev/null 2>&1; then \
		echo "❌ API server not running. Start it with 'make dev' first."; \
		exit 1; \
	fi
	python3 scripts/generate_postman_collection.py --url http://localhost:8000
	@echo "✅ Advanced API specification generated!"

test-workflow:
	@echo "🧪 Testing GitHub Actions workflow locally..."
	./scripts/test_workflow.sh

test-security:
	@echo "🔒 Testing security scanning tools locally..."
	./scripts/test_security_scan.sh
