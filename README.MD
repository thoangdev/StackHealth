# 🎯 Software Scorecard Dashboard - Stack Health

A comprehensive web application for tracking and visualizing software quality scorecards across four key areas: **Automation**, **Performance**, **Security**, and **CI/CD**. The system provides historic data tracking, PDF report generation, and trend analysis with both traditional deployment and Docker support.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Docker](https://img.shields.io/badge/Docker-Supported-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🧱 Tech Stack

### Backend
- **FastAPI** (Python) - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping (ORM)
- **SQLite** - Lightweight database for data persistence
- **ReportLab** - Professional PDF generation
- **Uvicorn** - ASGI server for running the FastAPI application

### Frontend
- **HTML5/CSS3/JavaScript** - Modern web technologies
- **Chart.js** - Interactive charts for trend visualization
- **Axios** - HTTP client for API communication

### Infrastructure
- **Docker & Docker Compose** - Containerized deployment
- **Nginx** - Web server and reverse proxy for production

## 📁 Project Structure

```
StackHealth/
├── 🔧 Backend (FastAPI)
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database models and configuration
│   ├── schemas.py           # Pydantic models for API validation
│   ├── crud.py              # Database operations
│   ├── pdf_generator.py     # PDF report generation
│   └── requirements.txt     # Python dependencies
├── 🎨 Frontend (HTML/JS/CSS)
│   ├── index.html           # Dashboard UI
│   └── app.js              # JavaScript application logic
├── 🐳 Docker Configuration
│   ├── Dockerfile           # Backend container configuration
│   ├── docker-compose.yml   # Multi-service orchestration
│   ├── nginx.conf          # Nginx configuration
│   └── .dockerignore       # Docker ignore rules
├── 🛠️ Scripts
│   ├── setup.sh            # Development environment setup
│   ├── start_backend.sh     # Start backend server
│   ├── docker-start.sh      # Start with Docker
│   ├── docker-stop.sh       # Stop Docker services
│   └── create_sample_data.py # Generate sample data
├── 📚 Documentation
│   └── docs/
│       └── PROJECT_OVERVIEW.md
├── 💾 Data
│   └── data/               # Database and persistent data
└── 📝 Project Files
    ├── README.md           # This file
    └── .dockerignore       # Docker ignore rules
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites**: Docker and Docker Compose installed

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd StackHealth
   ```

2. **Start with Docker**:
   ```bash
   ./scripts/docker-start.sh
   ```

3. **Access the application**:
   - 🌐 **Frontend Dashboard**: http://localhost:3000
   - 📚 **Backend API**: http://localhost:8000
   - 📖 **API Documentation**: http://localhost:8000/docs

4. **Create sample data** (optional):
   ```bash
   docker-compose exec backend python /app/scripts/create_sample_data.py
   ```

5. **Stop services**:
   ```bash
   ./scripts/docker-stop.sh
   ```

### Option 2: Traditional Development Setup

**Prerequisites**: Python 3.8+ and pip installed

1. **Setup environment**:
   ```bash
   cd scripts
   ./setup.sh
   ```

2. **Start backend**:
   ```bash
   ./start_backend.sh
   ```

3. **Open frontend**:
   - Open `frontend/index.html` in your browser
   - Or serve with: `python -m http.server 3000` (in frontend/ directory)

4. **Create sample data** (optional):
   ```bash
   cd scripts
   python create_sample_data.py
   ```

## 🗃️ Database Schema

### Project Table
- `id` (Primary Key)
- `name` (Unique) - Project identifier
- `description` (Optional) - Project description
- `created_at` - Timestamp

### Scorecard Table
- `id` (Primary Key)
- `project_id` (Foreign Key) - Links to project
- `date` - Scorecard submission date
- `automation_score` (0-100) - Automation quality score
- `performance_score` (0-100) - Performance quality score
- `security_score` (0-100) - Security quality score
- `cicd_score` (0-100) - CI/CD quality score
- `created_at` - Timestamp

### Feedback Table
- `id` (Primary Key)
- `scorecard_id` (Foreign Key) - Links to scorecard
- `area` - One of: automation, performance, security, cicd
- `comment` - User feedback text
- `tool_recommendation` - Recommended tools
- `marked_for_improvement` (Boolean) - Improvement flag
- `created_at` - Timestamp

## 📡 API Endpoints

### Projects
- `POST /projects` - Create a new project
- `GET /projects` - List all projects

### Scorecards
- `POST /scorecards` - Submit a new scorecard with feedback
- `GET /scorecards` - List all scorecards
- `GET /scorecards?project_id={id}` - Filter scorecards by project
- `GET /scorecards/{id}` - Get specific scorecard details
- `GET /scorecards/{id}/pdf` - Download PDF report

### Health Check
- `GET /` - API health check

## 💡 Key Features

### � Scorecard Submission
- ✅ Project selection from dropdown
- ✅ Date picker (defaults to today)
- ✅ Score input (0-100) for all four areas
- ✅ Optional feedback per area with comments
- ✅ Tool recommendation fields
- ✅ Mark areas for improvement checkboxes
- ✅ **Auto-recommendations** for scores < 70%

### � Data Visualization
- ✅ **Responsive table** with color-coded score badges
- ✅ **Interactive trend charts** using Chart.js
- ✅ **Project filtering** capabilities
- ✅ **Export to PDF** functionality
- ✅ **Real-time updates** via API integration

### 📄 Professional PDF Reports
Reports automatically include:
- ✅ Project name and submission date
- ✅ All four scores with color-coded ratings
- ✅ Feedback comments and recommendations
- ✅ Tool suggestions for improvement
- ✅ Highlighted areas marked for improvement
- ✅ Clean, professional formatting

### 🏗️ Project Management
- ✅ Create new projects with descriptions
- ✅ View all existing projects
- ✅ Automatic project linking to scorecards

### 🤖 Smart Recommendations

When scores fall below 70%, the system automatically suggests tools:

| Area | Recommended Tools |
|------|------------------|
| **🤖 Automation** | Playwright, Selenium, Cypress |
| **⚡ Performance** | k6, JMeter, Lighthouse |
| **🔒 Security** | OWASP ZAP, SonarQube, Snyk |
| **🔄 CI/CD** | GitHub Actions, Jenkins, GitLab CI |

## 🎨 UI/UX Features

### Modern Design
- 🎨 **Gradient header** with professional branding
- 📱 **Responsive design** for mobile and desktop
- 🃏 **Card-based layout** for better organization
- ✨ **Smooth animations** and hover effects

### User Experience
- 📋 **Tabbed interface** for organized navigation
- ✅ **Form validation** and error handling
- 🔄 **Loading states** and progress indicators
- 🚨 **Success/error alerts** with auto-dismiss
- 🎯 **Interactive elements** with visual feedback

### Data Visualization
- 🟢🟡🔴 **Color-coded score badges** (Green: 80+, Yellow: 60-79, Red: <60)
- 📈 **Multi-line trend charts** with legends
- 📊 **Clean, sortable tables**
- 📥 **One-click PDF export**

## � Docker Configuration

### Services
- **Backend**: FastAPI application with Python 3.9
- **Frontend**: Nginx serving static files with API proxy
- **Data**: Persistent volume for SQLite database

### Docker Commands
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# Execute commands in backend container
docker-compose exec backend python create_sample_data.py
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL` - Database connection string (default: SQLite)
- `PYTHONPATH` - Python module path

### Development vs Production
- **Development**: Direct file serving, CORS enabled for all origins
- **Production**: Nginx proxy, specific CORS origins, optimized builds

## 🚀 Deployment Options

### Local Development
1. Traditional Python virtual environment
2. Docker development containers

### Production Deployment
1. **Docker Compose** (recommended for small to medium deployments)
2. **Kubernetes** (for large-scale deployments)
3. **Cloud platforms** (AWS, GCP, Azure with container services)

### Cloud Deployment Example
```bash
# For cloud deployment, update docker-compose.yml with:
# - Production database (PostgreSQL, MySQL)
# - Environment-specific configurations
# - SSL/TLS certificates
# - Load balancing setup
```

## 🧪 Testing

### Manual Testing
1. **Submit scorecards** with various score combinations
2. **Test PDF generation** for different scenarios
3. **Verify trend charts** with multiple data points
4. **Test project filtering** functionality

### Sample Data
The `create_sample_data.py` script generates:
- 4 realistic projects
- 24 scorecards with varied scores
- Feedback and improvement recommendations
- Historical data spanning 30 days

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python3 --version

# Reinstall dependencies
pip install -r backend/requirements.txt
```

**Docker issues:**
```bash
# Check Docker status
docker --version
docker-compose --version

# Rebuild containers
docker-compose down
docker-compose up --build
```

**Frontend API connection:**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify API base URL configuration

### Getting Help
1. Check the [API documentation](http://localhost:8000/docs) when backend is running
2. Review browser console for JavaScript errors
3. Check Docker logs: `docker-compose logs -f`
4. Verify all services are running: `docker-compose ps`

## 🎯 Future Enhancements

### Short Term
- [ ] User authentication and authorization
- [ ] Data export to CSV/Excel
- [ ] Email notifications for low scores
- [ ] Advanced filtering and search

### Long Term
- [ ] Multi-tenant support for teams
- [ ] Integration with CI/CD pipelines
- [ ] Advanced analytics and insights
- [ ] Mobile application
- [ ] Real-time collaboration features
- [ ] Integration with popular development tools

---

## 🎉 **Ready for Production!**

This Software Scorecard Dashboard is **production-ready** with:
- ✅ **Complete functionality** - All requirements implemented
- ✅ **Professional design** - Modern, responsive UI
- ✅ **Docker support** - Easy deployment and scaling
- ✅ **Comprehensive documentation** - Everything you need to get started
- ✅ **Sample data** - Ready for immediate testing

**Start tracking your software quality metrics today!** 🚀
