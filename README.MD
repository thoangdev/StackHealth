# 🚀 StackHealth Scorecard Platform v2.0

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Security](https://img.shields.io/badge/security-OWASP%20SAMM-red.svg)
![DORA](https://img.shields.io/badge/DORA-metrics-purple.svg)

**Enterprise-grade Software Scorecard Dashboard with DORA Metrics, OWASP SAMM Security Assessment, Performance Testing Integration, and Advanced CI/CD Pipeline Evaluation**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API Reference](#-api-reference) • [Contributing](#-contributing)

</div>

## 🌟 Features

### 📊 **DORA Metrics Integration**
- **Deployment Frequency** assessment (On-demand to Monthly)
- **Lead Time for Changes** tracking (Hours to Months)
- **Mean Time to Recovery** measurement (Minutes to Weeks)
- **Change Failure Rate** analysis (0% to 30%+)

### 🔒 **OWASP SAMM Security Assessment**
- 30-point comprehensive security evaluation
- Static/Dynamic Application Security Testing (SAST/DAST)
- Software Composition Analysis (SCA) integration
- Threat modeling and secure design practices
- Security culture and governance assessment

### 🔧 **Advanced CI/CD Pipeline Evaluation**
- 45-point pipeline maturity assessment with DORA metrics
- Infrastructure as Code evaluation
- Advanced deployment strategies (Blue-Green, Canary)
- Security integration in pipelines
- GitOps and modern practices assessment

### 🤖 **Comprehensive Test Automation Assessment**
- 40-point automation maturity evaluation with coverage bonuses
- Test framework architecture and reliability analysis
- API and functional test coverage tracking (0-100%)
- Automated testing environment assessment
- CI/CD integration and advanced reporting capabilities

### ⚡ **Performance Testing Integration**
- 30-point performance testing scorecard
- Load, stress, spike, and soak testing evaluation
- Real-time performance monitoring and alerting systems
- Production-like environment testing assessment
- SLA/SLO definition and trend analysis

### 🏢 **Enterprise Features**
- **JWT Authentication** with secure token management
- **Role-based Access Control** (Admin, User roles)
- **Professional PDF Reports** with detailed breakdowns
- **Historical Trend Analysis** with 90-day tracking
- **Independent Category Scoring** - Each category scored 0-100%
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

### 🔒 Security Scorecard (30 points)
**Static & Dynamic Testing (12 points)**:
- **Static Application Security Testing (SAST)** (3 pts)
  - Automated static code analysis for vulnerabilities
- **Dynamic Application Security Testing (DAST)** (3 pts)  
  - Runtime security testing of applications
- **CI/CD Pipeline Integration** (4 pts)
  - SAST/DAST integrated into deployment pipeline (highest impact)
- **Security Finding Management** (2 pts)
  - Systematic triage and remediation process

**Dependency & Secrets Management (8 points)**:
- **Secrets Scanning** (2 pts)
  - Automated credential and secret detection (critical security gap)
- **Software Composition Analysis (SCA)** (3 pts)
  - Dependency vulnerability monitoring (supply chain security)
- **Critical Vulnerability Alerting** (3 pts)
  - Real-time CVE and security issue notifications

**Security Culture & Governance (10 points)**:
- **Security Reviews & Threat Modeling** (3 pts)
  - Regular security assessments and threat analysis
- **Compliance Standards** (2 pts)
  - Adherence to FedRAMP, SOC2, or similar frameworks
- **Secure Coding Training** (2 pts)
  - Developer security education programs
- **Responsible Disclosure Program** (1 pt)
  - Bug bounty or vulnerability disclosure process
- **Security Champions Program** (2 pts)
  - Dedicated security advocates in development teams

### 🤖 Automation Scorecard (40 points)
**Test Automation Foundation (15 points)**:
- **Automated Testing Implementation** (2 pts)
  - Basic automated testing in place
- **Testing Framework Foundation** (3 pts)
  - Structured framework with clear patterns (critical for scaling)
- **Dedicated Automation Environment** (2 pts)  
  - Isolated environment for test execution
- **Source Code Management** (3 pts)
  - Automation code properly version controlled (essential practice)
- **Development Environment Setup** (1 pt)
  - Quick local development machine setup (<1 day)
- **External Updates Management** (2 pts)
  - Framework stays current with dependencies
- **Test Reporting & Analytics** (2 pts)
  - Comprehensive automated test reports with trends

**Test Design & Maintenance (13 points)**:
- **Test Data Management** (2 pts)
  - Tests use seeded data appropriately
- **Test Independence** (-5 pts if violated)
  - Tests don't depend on previous test data (critical anti-pattern)
- **Data Re-seeding Capability** (3 pts)
  - Easy data reset and re-seeding processes (key for reliability)
- **Test Subset Execution** (3 pts)
  - Run specific test groups without code changes (efficiency)
- **Rapid Test Updates** (2 pts)
  - Tests updated within 1 day of application changes
- **Database Automation** (2 pts)
  - Automated database connections and operations
- **Cross-Browser/Platform Testing** (2 pts)
  - Multi-environment test execution
- **Parallel Test Execution** (2 pts)
  - Tests run in parallel for faster feedback
- **Test Flakiness Management** (2 pts)
  - Processes to identify and fix unreliable tests

**CI/CD Integration & Deployment Testing (12 points)**:
- **Post-Deploy Sanity Testing** (3 pts)
  - Automated verification after deployments (critical for quality gates)
- **Smoke Testing Independence** (-2 pts if violated)
  - Sanity tests don't rely on full functional testing
- **Build Verification Testing** (3 pts)
  - Automated smoke tests for build verification
- **Performance Test Integration** (2 pts)
  - Performance tests integrated into CI/CD
- **Security Test Integration** (2 pts)
  - Security scans integrated into automation pipeline
- **Notification Integration** (1 pt)
  - Results feed into Slack/Teams/Email
- **Test Results Dashboard** (2 pts)
  - Real-time visibility into test execution and trends
- **Automated Test Scheduling** (1 pt)
  - Scheduled regression and maintenance testing

**Test Coverage Assessment (bonus points)**:
- **API Test Coverage** (0-10 bonus pts based on coverage)
  - 0%: 0 points | 1-20%: 1 point | 20-40%: 2 points
  - 40-60%: 4 points | 60-80%: 7 points | 80-100%: 10 points
- **Functional (GUI) Test Coverage** (0-5 bonus pts based on coverage)
  - 0%: 0 points | 1-20%: 1 point | 20-40%: 2 points
  - 40-70%: 3 points | 70-100%: 5 points
- **Integration Test Coverage** (0-3 bonus pts based on coverage)
  - 0%: 0 points | 1-50%: 1 point | 50-80%: 2 points | 80-100%: 3 points

### ⚡ Performance Scorecard (30 points)
**Performance Strategy & Planning (10 points)**:
- **Performance Requirements Definition** (3 pts)
  - Clear SLA/SLO definitions with measurable targets
- **Regular Performance Testing** (2 pts)
  - Systematic performance testing practices
- **Performance Budget & Thresholds** (2 pts)
  - Defined latency, throughput, and resource utilization limits
- **Performance Trend Analysis** (3 pts)
  - Historical baseline tracking and regression detection

**Testing Implementation & Tools (12 points)**:
- **Dedicated Performance Tools** (2 pts)
  - Professional tools (K6, JMeter, Artillery, etc.)
- **CI/CD Integration** (4 pts)
  - Performance testing in deployment pipeline (critical for early detection)
- **Production-like Environment Testing** (3 pts)
  - Realistic testing environments with prod-scale data
- **Load Testing Coverage** (1-3 pts based on test types)
  - Smoke: 1 pt | Load: 2 pts | Stress: 3 pts
- **Advanced Testing Types** (bonus 2 pts each)
  - Spike Testing: +2 pts | Soak/Endurance Testing: +2 pts

**Monitoring & Observability (8 points)**:
- **Real-time Performance Monitoring** (2 pts)
  - Live application performance monitoring (APM)
- **Core Metrics Tracking** (2 pts)
  - Latency, throughput, error rate monitoring
- **Resource Utilization Monitoring** (1 pt)
  - CPU, memory, disk, network monitoring
- **Performance Dashboard & Visualization** (2 pts)
  - Performance data visualization (Grafana, New Relic, etc.)
- **Automated Performance Alerting** (1 pt)
  - Threshold breach and regression notifications

### 🔄 CI/CD Scorecard (45 points)
**DORA Metrics (20 points)**:
- **Deployment Frequency** (5 pts)
  - On-demand: 5 pts | Daily: 4 pts | Weekly: 2 pts | Monthly: 1 pt
- **Lead Time for Changes** (5 pts)
  - <1 hour: 5 pts | <1 day: 4 pts | <1 week: 2 pts | >1 week: 1 pt
- **Mean Time to Recovery** (5 pts)
  - <1 hour: 5 pts | <1 day: 4 pts | <1 week: 2 pts | >1 week: 1 pt
- **Change Failure Rate** (5 pts)
  - 0-5%: 5 pts | 6-15%: 4 pts | 16-30%: 2 pts | >30%: 1 pt

**Pipeline Foundation (15 points)**:
- **Automated Build Process** (3 pts)
  - Consistent, repeatable build automation
- **Automated Testing Integration** (4 pts)
  - Unit, integration, and functional tests in pipeline
- **Code Quality Gates** (3 pts)
  - Automated code quality checks and enforcement
- **Security Integration** (3 pts)
  - Security scans integrated into pipeline
- **Artifact Management** (2 pts)
  - Versioned artifact storage and promotion

**Deployment & Release Management (10 points)**:
- **Automated Deployment Pipeline** (3 pts)
  - Consistent deployment across environments
- **Environment Promotion Strategy** (2 pts)
  - Clear dev → staging → production progression
- **Rollback Capability** (3 pts)
  - Automated rollback and recovery procedures
- **Feature Flag Management** (2 pts)
  - Dynamic feature toggling and gradual rollouts

**Advanced Practices (bonus points)**:
- **Blue-Green Deployment** (bonus 3 pts)
  - Zero-downtime deployment strategy
- **Canary Releases** (bonus 3 pts)
  - Gradual release with automated monitoring
- **Infrastructure as Code** (bonus 4 pts)
  - Automated infrastructure provisioning and management
- **GitOps Implementation** (bonus 2 pts)
  - Git-driven operations and deployment

## 🎯 Scoring System

### Individual Category Scoring
Each category is scored independently on a 0-100% scale:

- **🔒 Security Scorecard**: 30 points maximum (scored as percentage)
- **🤖 Automation Scorecard**: 40 points + coverage bonuses (scored as percentage)
- **⚡ Performance Scorecard**: 30 points (scored as percentage)
- **🔄 CI/CD Scorecard**: 45 points + advanced practice bonuses (scored as percentage)

### Score Interpretation (Per Category)
- **90-100%**: 🟢 Excellent - Industry leading practices
- **75-89%**: 🔵 Good - Strong foundation with room for improvement
- **60-74%**: 🟡 Average - Basic practices in place
- **40-59%**: 🟠 Below Average - Significant improvements needed
- **0-39%**: 🔴 Critical - Immediate attention required

### Category-Specific Scoring Logic

**🔒 Security (30 points = 100%)**:
- Static & Dynamic Testing: 40% weight
- Dependency & Secrets Management: 27% weight
- Security Culture & Governance: 33% weight

**🤖 Automation (40 points + bonuses = 100%+)**:
- Test Automation Foundation: 37.5% weight
- Test Design & Maintenance: 32.5% weight
- CI/CD Integration & Deployment Testing: 30% weight
- Coverage bonuses can exceed 100% for exceptional automation

**⚡ Performance (30 points = 100%)**:
- Performance Strategy & Planning: 33% weight
- Testing Implementation & Tools: 40% weight
- Monitoring & Observability: 27% weight

**🔄 CI/CD (45 points + bonuses = 100%+)**:
- DORA Metrics: 44% weight (industry gold standard)
- Pipeline Foundation: 33% weight
- Deployment & Release Management: 23% weight
- Advanced practice bonuses can exceed 100% for cutting-edge implementations

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

**Made with ❤️ for the QA, DevOps, and Security Community**

[⭐ Star us on GitHub](https://github.com/thoangdev/StackHealth) • [🐛 Report Bug](https://github.com/thoangdev/StackHealth/issues) • [💡 Request Feature](https://github.com/thoangdev/StackHealth/issues)

</div>
