# 🛠️ Development Guide

Welcome to StackHealth development! This guide will help you get started with contributing to the project.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ 
- Git
- Docker (optional, for containerized development)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/thoangdev/stackhealth.git
cd stackhealth

# Run the setup script
./scripts/setup-dev.sh

# Or use Make
make setup
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up pre-commit hooks
- Initialize the database
- Run tests to verify setup

## 🏗️ Project Structure

```
stackhealth/
├── 🔧 backend/                 # FastAPI application
│   ├── main.py                # Main FastAPI app
│   ├── auth.py                # Authentication
│   ├── crud.py                # Database operations
│   ├── database.py            # Database models
│   ├── health.py              # Health check endpoints
│   ├── pdf_generator.py       # PDF report generation
│   ├── schemas.py             # Pydantic models
│   └── tests/                 # Test suite
├── 🎨 frontend/               # Web interface
├── ⚙️ config/                 # Configuration files
├── 📚 docs/                   # Documentation
├── 🔄 scripts/               # Development scripts
└── 🚢 deployment/            # Production deployment
```

## 🧪 Testing

### Running Tests

```bash
# All tests with coverage
make test

# Unit tests only
make test-unit

# Integration tests only
make test-int

# Security tests only
make test-security
```

### Writing Tests

Tests are located in `backend/tests/`. We use:
- **pytest** for test framework
- **pytest-cov** for coverage
- **httpx** for API testing
- **pytest-asyncio** for async tests

Example test:
```python
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Test Categories

Use markers to categorize tests:
```python
@pytest.mark.unit
def test_user_creation():
    pass

@pytest.mark.integration 
def test_api_integration():
    pass

@pytest.mark.security
def test_authentication():
    pass
```

## 📝 Code Style

We maintain consistent code style using:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking
- **bandit** for security scanning

### Formatting Code

```bash
# Format all code
make format

# Run linting
make lint

# Run pre-commit hooks
make pre-commit
```

### Pre-commit Hooks

Pre-commit hooks run automatically on each commit and check:
- Code formatting (Black)
- Import sorting (isort)
- Linting (flake8)
- Type checking (mypy)
- Security scanning (bandit)
- General file checks

## 🚀 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write code following our style guidelines
- Add tests for new functionality
- Update documentation if needed

### 3. Test Your Changes
```bash
make test
make lint
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new feature"
```

Pre-commit hooks will run automatically.

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 🐳 Docker Development

### Build and Run
```bash
# Build image
make build

# Run with Docker Compose
make deploy

# Development mode
make deploy-dev
```

### Health Checks
```bash
# Check application health
make health

# Or directly
curl http://localhost:8000/health
```

## 📊 Database

### Initialize Database
```bash
make db-init
```

### Reset Database
```bash
make db-reset
```

### Migrations (if using Alembic)
```bash
cd backend
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

## 🔧 Configuration

Configuration files are in the `config/` directory:
- `.env.example` - Template with all options
- `.env.development` - Development settings  
- `.env.production` - Production settings

Copy and modify as needed:
```bash
cp config/.env.example config/.env.development
```

## 📚 API Documentation

- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🐛 Debugging

### VS Code Setup
The project includes VS Code configuration:
- Debugger settings in `.vscode/launch.json`
- Recommended extensions in `.vscode/extensions.json`
- Task configurations in `.vscode/tasks.json`

### Common Issues

**Import errors**: Make sure virtual environment is activated
```bash
source venv/bin/activate
```

**Database errors**: Reset and initialize database
```bash
make db-reset
```

**Port conflicts**: Change port in config or kill existing processes
```bash
lsof -ti:8000 | xargs kill -9
```

## 🤝 Contributing Guidelines

### Commit Messages
Follow conventional commits:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance tasks

### Code Review
- All changes require review
- Tests must pass
- Coverage should not decrease
- Follow style guidelines

### Documentation
- Update README if needed
- Add docstrings to new functions
- Update API documentation
- Include examples for new features

## 📞 Getting Help

- Check existing issues on GitHub
- Review this documentation
- Ask questions in pull requests
- Contact maintainers

## 🎯 Development Commands Reference

| Command | Description |
|---------|-------------|
| `make setup` | Set up development environment |
| `make test` | Run all tests |
| `make lint` | Run code linting |
| `make format` | Format code |
| `make dev` | Start development server |
| `make build` | Build Docker image |
| `make deploy` | Deploy with Docker |
| `make health` | Check application health |
| `make clean` | Clean temporary files |

Happy coding! 🚀
