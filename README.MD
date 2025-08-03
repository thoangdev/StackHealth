# 🚀 StackHealth Scorecard Platform v2.0

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Security](https://img.shields.io/badge/security-OWASP%20SAMM-red.svg)
![DORA](https://img.shields.io/badge/DORA-metrics-purple.svg)

**Enterprise-grade Software Scorecard Dashboard with DORA Metrics, OWASP SAMM Security Assessment, and Advanced CI/CD Pipeline Evaluation**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API Reference](#-api-reference) • [Contributing](#-contributing)

</div>

## 🌟 Features

### 📊 **DORA Metrics Integration**
- **Deployment Frequency** assessment (On-demand to Monthly)
- **Lead Time for Changes** tracking (Hours to Months)
- **Mean Time to Recovery** measurement (Minutes to Weeks)
- **Change Failure Rate** analysis (0% to 30%+)

### 🔒 **OWASP SAMM Security Assessment**
- 14-field comprehensive security evaluation
- Static/Dynamic Application Security Testing (SAST/DAST)
- Software Composition Analysis (SCA) integration
- Threat modeling and secure design practices
- Compliance tracking (SOC2, FedRAMP, etc.)

### 🔧 **Advanced CI/CD Pipeline Evaluation**
- Core pipeline maturity assessment (20+ criteria)
- Infrastructure as Code evaluation
- Advanced deployment strategies (Blue-Green, Canary)
- Security integration in pipelines
- Configuration management assessment

### 🏢 **Enterprise Features**
- **JWT Authentication** with secure token management
- **Role-based Access Control** (Admin, User roles)
- **Professional PDF Reports** with detailed breakdowns
- **Historical Trend Analysis** with 90-day tracking
- **Weighted Scoring System** with industry benchmarks
- **RESTful API** with OpenAPI/Swagger documentation

### 🚀 **DevOps Ready**
- **Docker containerization** with multi-stage builds
- **Kubernetes deployment** configurations
- **Terraform infrastructure** as code
- **GitHub Actions CI/CD** pipelines
- **Security scanning** integration
- **Health checks** and monitoring

## 🏃 Quick Start

### Prerequisites
- Python 3.9+
- Git
- Docker (optional)

### 1. Clone and Setup
```bash
git clone https://github.com/thoangdev/StackHealth.git
cd StackHealth

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Configuration
```bash
# Copy environment configuration
cp config/.env.example config/.env.development

# Edit configuration (optional)
nano config/.env.development
```

### 3. Initialize Database
```bash
cd backend
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 4. Generate Sample Data
```bash
python ../scripts/create_enhanced_sample_data.py
```

### 5. Start the Application
```bash
# Start backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In a new terminal, open frontend
open ../frontend/index.html
```

### 6. Login and Explore
- **URL**: http://localhost:8000 (API) / Open `frontend/index.html` (UI)
- **Demo Login**: `admin@company.com` / `admin123`
- **Swagger Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
StackHealth/
├── 🔧 backend/                 # FastAPI application
│   ├── auth.py                # JWT authentication
│   ├── crud.py                # Database operations
│   ├── database.py            # Database models
│   ├── main.py                # FastAPI app
│   ├── pdf_generator.py       # PDF report generation
│   ├── schemas.py             # Pydantic models
│   ├── requirements.txt       # Python dependencies
│   └── tests/                 # Test suite
├── 🎨 frontend/               # Web interface
│   ├── index.html            # Main application
│   └── app.js                # JavaScript logic
├── 🚢 deployment/             # Production deployment
│   ├── kubernetes.yaml       # K8s configurations
│   ├── terraform/            # Infrastructure as code
│   └── deploy.sh             # Deployment script
├── 📝 docs/                   # Documentation
├── 🔄 scripts/               # Utility scripts
├── ⚙️ config/                # Configuration files
│   ├── .env.example          # Environment template
│   ├── .env.development      # Development config
│   └── .env.production       # Production config
├── 🧪 .github/               # GitHub workflows
│   ├── workflows/            # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/       # Issue templates
│   └── pull_request_template.md
├── 🐳 Dockerfile             # Container configuration
└── 📋 requirements files     # Dependencies
```

## 🛠️ Development

### Local Development Setup
```bash
# Install development dependencies
pip install -r backend/requirements-dev.txt

# Run tests
cd backend
pytest

# Code formatting
black .
isort .

# Linting
flake8 .

# Type checking
mypy .
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest -m "unit"          # Unit tests only
pytest -m "integration"   # Integration tests only
pytest -m "security"      # Security tests only
```

## 🐳 Docker Deployment

### Quick Docker Run
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t stackhealth .
docker run -p 8000:8000 stackhealth
```

### Production Deployment
```bash
# Deploy to Kubernetes
kubectl apply -f deployment/kubernetes.yaml

# Or use the deployment script
./deployment/deploy.sh deploy
```

## 📊 Assessment Categories

### 🔒 Security Scorecard (25 points)
Based on OWASP Software Assurance Maturity Model (SAMM):
- Static/Dynamic Application Security Testing
- Software Composition Analysis
- Secrets scanning and management
- Threat modeling processes
- Security training and compliance

### 🤖 Automation Scorecard (10 points)
- Continuous Integration pipelines
- Automated testing frameworks
- Deployment automation
- Infrastructure as Code
- Monitoring and alerting

### ⚡ Performance Scorecard (9 points)
- Load testing implementation
- Performance monitoring tools
- Caching strategies
- Database optimization
- CDN usage and optimization

### 🔄 CI/CD Scorecard (42 points)
**DORA Metrics (16 points)**:
- Deployment Frequency (4 pts)
- Lead Time for Changes (4 pts)
- Mean Time to Recovery (4 pts)
- Change Failure Rate (4 pts)

**Pipeline Maturity (26 points)**:
- Core pipeline components (16 pts)
- Advanced capabilities (10 pts)

## 🎯 Scoring System

### Score Interpretation
- **90-100%**: 🟢 Excellent - Industry leading practices
- **70-89%**: 🔵 Good - Strong foundation with room for improvement
- **50-69%**: 🟡 Average - Basic practices in place
- **30-49%**: 🟠 Below Average - Significant improvements needed
- **0-29%**: 🔴 Critical - Immediate attention required

### Weighted Scoring
Each category uses industry-standard weights:
- **Security**: Emphasizes critical security practices (SAST/DAST: 3pts each)
- **CI/CD**: DORA metrics weighted heavily (4pts each)
- **Performance**: Monitoring and testing prioritized
- **Automation**: CI/CD integration valued highest

## 📚 Documentation

- **[📖 Complete Documentation](docs/)** - Full documentation index
- **[👤 User Guide](docs/USER_GUIDE.md)** - End user instructions
- **[🛠️ Development Guide](docs/DEVELOPMENT.md)** - Developer setup and workflow
- **[🤝 Contributing Guide](docs/CONTRIBUTING.md)** - Development guidelines
- **[🔒 Security Guide](docs/SECURITY.md)** - Security best practices
- **[📝 Changelog](docs/CHANGELOG.md)** - Version history
- **[🏗️ Project Overview](docs/PROJECT_OVERVIEW.md)** - Technical architecture

## 🔗 API Reference

### Authentication
```bash
# Register new user
POST /auth/register
{
  "email": "user@company.com",
  "password": "secure_password"
}

# Login
POST /auth/login
{
  "email": "user@company.com", 
  "password": "secure_password"
}
```

### Scorecards
```bash
# Create scorecard
POST /scorecards
Authorization: Bearer {token}
{
  "product_id": 1,
  "category": "security",
  "breakdown": {
    "sast": true,
    "dast": false,
    "sast_dast_in_ci": true
  }
}

# Get trends
GET /trends/{product_id}/{category}?days=90
Authorization: Bearer {token}
```

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Workflow
- Follow [Conventional Commits](https://conventionalcommits.org/)
- Ensure tests pass (`pytest`)
- Maintain code coverage (>80%)
- Update documentation as needed

## 🔒 Security

Security is a top priority. Please see our [Security Policy](SECURITY.md) for:
- Vulnerability reporting process
- Security best practices
- Supported versions
- Security features

To report security vulnerabilities: **security@stackhealth.com**

## 📈 Roadmap

### v2.1.0 (Q3 2025)
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant support
- [ ] SSO integration (SAML, OAuth)
- [ ] Advanced notification system

### v2.2.0 (Q4 2025)
- [ ] Machine learning recommendations
- [ ] Industry benchmarking
- [ ] API rate limiting
- [ ] Advanced reporting templates

### v3.0.0 (2026)
- [ ] Microservices architecture
- [ ] Real-time collaboration
- [ ] Mobile application
- [ ] Advanced integrations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **DORA Research**: Built on Google's DevOps Research and Assessment metrics
- **OWASP SAMM**: Security assessment based on OWASP Software Assurance Maturity Model
- **DevOps Community**: Inspired by industry best practices and community feedback

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/thoangdev/StackHealth/issues)
- **Discussions**: [GitHub Discussions](https://github.com/thoangdev/StackHealth/discussions)
- **Email**: support@stackhealth.com

---

<div align="center">

**Made with ❤️ for the DevOps and Security Community**

[⭐ Star us on GitHub](https://github.com/thoangdev/StackHealth) • [🐛 Report Bug](https://github.com/thoangdev/StackHealth/issues) • [💡 Request Feature](https://github.com/thoangdev/StackHealth/issues)

</div>
