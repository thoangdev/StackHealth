# Contributing to StackHealth Scorecard Platform

We welcome contributions to the StackHealth Scorecard Platform! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to team@stackhealth.com.

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+ (for frontend development)
- Git
- VS Code (recommended)

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/yourusername/StackHealth.git
   cd StackHealth
   ```

2. **Environment Setup**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r backend/requirements.txt
   ```

3. **Configuration**

   ```bash
   cp .env.example .env.development
   # Edit .env.development with your settings
   ```

4. **Database Setup**

   ```bash
   cd backend
   python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
   ```

5. **Run Development Server**
   ```bash
   python -m uvicorn main:app --reload
   ```

## Development Process

### Branch Naming

- `feature/feature-name` - New features
- `bugfix/issue-description` - Bug fixes
- `hotfix/critical-issue` - Critical production fixes
- `docs/update-description` - Documentation updates

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

Examples:

```
feat(api): add DORA metrics endpoint
fix(auth): resolve JWT expiration handling
docs(readme): update installation instructions
```

## Pull Request Process

1. **Create Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**

   - Write clean, readable code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**

   ```bash
   # Run backend tests
   cd backend
   python -m pytest

   # Run linting
   flake8 .
   black .
   ```

4. **Submit Pull Request**
   - Provide clear description
   - Reference related issues
   - Include screenshots for UI changes
   - Ensure CI passes

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-reviewed the code
- [ ] Added tests for changes
- [ ] Updated documentation
```

## Coding Standards

### Python (Backend)

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use Black for formatting
- Use flake8 for linting

```python
# Good
def calculate_score(breakdown: Dict[str, Any], category: str) -> float:
    """Calculate overall score based on breakdown fields."""
    pass

# Avoid
def calc_score(breakdown, category):
    pass
```

### JavaScript (Frontend)

- Use ES6+ features
- Consistent indentation (2 spaces)
- Meaningful variable names
- Add JSDoc comments for functions

```javascript
// Good
/**
 * Updates scorecard fields based on selected category
 * @param {string} category - The scorecard category
 */
updateScorecardFields(category) {
    // Implementation
}

// Avoid
updateFields(cat) {
    // Implementation
}
```

### Database

- Use descriptive table/column names
- Include proper indexes
- Add foreign key constraints
- Document schema changes

## Testing

### Backend Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_auth.py
```

### Frontend Testing

```bash
# Manual testing checklist
- [ ] Authentication flow
- [ ] Scorecard creation
- [ ] PDF generation
- [ ] Responsive design
- [ ] Error handling
```

### Test Guidelines

- Write tests for new features
- Maintain >80% code coverage
- Use descriptive test names
- Test both success and failure cases

## Documentation

### Code Documentation

- Add docstrings to functions/classes
- Include parameter and return type information
- Provide usage examples

### API Documentation

- Update OpenAPI/Swagger specs
- Document all endpoints
- Include request/response examples

### User Documentation

- Update README for new features
- Provide clear setup instructions
- Include troubleshooting section

## Release Process

1. **Version Bump**

   - Update version in relevant files
   - Follow semantic versioning

2. **Changelog**

   - Document all changes
   - Categorize by type (Added, Changed, Fixed, Removed)

3. **Testing**

   - Full regression testing
   - Performance testing
   - Security review

4. **Deployment**
   - Deploy to staging
   - Production deployment
   - Monitor for issues

## Getting Help

- **Documentation**: Check existing docs first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: team@stackhealth.com for sensitive matters

## Recognition

Contributors will be acknowledged in:

- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to StackHealth Scorecard Platform! 🚀
