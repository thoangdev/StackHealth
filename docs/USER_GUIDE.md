# 🎯 User Guide - StackHealth Scorecard Platform

Welcome to StackHealth! This guide will help you get started with tracking and improving your software quality metrics.

## 🚀 Quick Start

### For End Users

#### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/thoangdev/stackhealth.git
cd stackhealth

# Start the application
docker-compose up -d

# Access the application
open http://localhost:3000
```

#### Option 2: Traditional Setup
```bash
# Clone and setup
git clone https://github.com/thoangdev/stackhealth.git
cd stackhealth
./scripts/setup.sh

# Start the backend
./scripts/start_backend.sh

# Open the frontend
open frontend/index.html
```

### First Login
1. Navigate to the application URL
2. Register a new account or use demo credentials
3. Start creating your first scorecard!

## 📊 Understanding StackHealth

### What is a Scorecard?
A scorecard is an assessment of your software's quality across four key areas:
- **🔒 Security** - OWASP SAMM-based security assessment
- **🚀 Performance** - System performance and monitoring
- **🤖 Automation** - CI/CD pipeline maturity
- **📈 DevOps** - DORA metrics and practices

### Scoring System
- **90-100%**: 🟢 Excellent - Industry leading
- **80-89%**: 🟡 Good - Above average
- **70-79%**: 🟠 Fair - Needs improvement  
- **Below 70%**: 🔴 Poor - Immediate attention required

## 🏗️ Core Features

### 1. Product Management
Create and manage products (applications, services, systems):
- Add product name and description
- Track multiple products separately
- View product-specific trends

### 2. Scorecard Submission
Submit assessments for each product:
- Select assessment category
- Answer category-specific questions
- Provide feedback and comments
- Get automatic tool recommendations

### 3. Trend Analysis
Track improvement over time:
- View historical score trends
- Compare across categories
- Identify improvement patterns
- Export trend data

### 4. PDF Reports
Generate professional reports:
- Detailed breakdowns by category
- Tool recommendations
- Historical comparisons
- Shareable with stakeholders

## 📋 Assessment Categories

### 🔒 Security Assessment (OWASP SAMM)
Evaluates 14 security practice areas:
- **Governance**: Security strategy and metrics
- **Design**: Threat modeling and security requirements
- **Implementation**: Security testing and secure coding
- **Verification**: Architecture assessment and testing
- **Operations**: Incident management and monitoring

**Key Questions:**
- Do you perform static application security testing (SAST)?
- Is dynamic application security testing (DAST) integrated?
- Are security requirements defined for each release?
- Do you have threat modeling processes?

### 🚀 Performance Assessment
Focuses on system performance and monitoring:
- Performance testing strategies
- Monitoring and alerting
- Resource optimization
- Scalability planning

**Key Questions:**
- Do you perform load testing?
- Are performance metrics monitored?
- Do you have alerting for performance issues?
- Is performance testing automated?

### 🤖 Automation Assessment
Evaluates CI/CD pipeline maturity:
- Build automation
- Testing automation
- Deployment automation
- Infrastructure as Code

**Key Questions:**
- Are builds automated and triggered by commits?
- Is testing automated in your pipeline?
- Do you use Infrastructure as Code?
- Are deployments automated?

### 📈 DevOps Assessment (DORA Metrics)
Based on Google's DORA research:
- **Deployment Frequency**: How often you deploy
- **Lead Time for Changes**: Time from commit to production
- **Mean Time to Recovery**: How quickly you recover from failures
- **Change Failure Rate**: Percentage of deployments causing failures

**Performance Levels:**
- **Elite**: Multiple deployments per day, <1 hour lead time
- **High**: Between once per week and once per month
- **Medium**: Between once per month and once every 6 months
- **Low**: Fewer than once per six months

## 🎯 Getting Started Workflow

### Step 1: Create Your First Product
1. Go to "Manage Products" tab
2. Click "Add New Product"
3. Enter product name and description
4. Save the product

### Step 2: Submit Your First Scorecard
1. Go to "Submit Scorecard" tab
2. Select your product
3. Choose an assessment category
4. Answer the questions honestly
5. Add any feedback or comments
6. Submit the scorecard

### Step 3: View Results
1. Go to "View Scorecards" tab
2. See your score and breakdown
3. Review tool recommendations
4. Export PDF report if needed

### Step 4: Track Progress
1. Submit regular scorecards (weekly/monthly)
2. Monitor trend charts
3. Focus on areas needing improvement
4. Celebrate improvements!

## 💡 Best Practices

### Assessment Frequency
- **Security**: Monthly assessments
- **Performance**: Weekly during active development
- **Automation**: After each major pipeline change
- **DevOps**: Quarterly for DORA metrics

### Team Involvement
- Involve different team members for diverse perspectives
- Have security experts assess security category
- Include DevOps engineers for automation assessments
- Get product owners involved in DevOps metrics

### Action Planning
- Focus on one category at a time
- Use tool recommendations as starting points
- Set realistic improvement targets
- Review progress regularly

## 🛠️ Tool Recommendations

StackHealth automatically suggests tools based on your scores:

### Security Tools
- **SAST**: SonarQube, CodeQL, Checkmarx
- **DAST**: OWASP ZAP, Burp Suite, Veracode
- **SCA**: Snyk, WhiteSource, Black Duck
- **Secrets**: GitLeaks, TruffleHog, detect-secrets

### Performance Tools
- **Load Testing**: k6, JMeter, Artillery
- **Monitoring**: Prometheus, Grafana, New Relic
- **APM**: Datadog, AppDynamics, Dynatrace

### Automation Tools
- **CI/CD**: GitHub Actions, Jenkins, GitLab CI
- **Testing**: Playwright, Cypress, Selenium
- **IaC**: Terraform, Ansible, CloudFormation

## 📊 Understanding Your Reports

### Score Breakdown
Each category shows:
- Overall percentage score
- Individual question scores
- Weighted importance of each area
- Comparison to industry benchmarks

### Trend Analysis
Trend charts display:
- Score progression over time
- Identification of improvement/regression
- Visual patterns and seasonality
- Goal tracking progress

### Recommendations
Tool suggestions include:
- Category-specific recommendations
- Open source vs. commercial options
- Implementation difficulty
- Integration complexity

## 🔧 Configuration and Customization

### Scoring Weights
Adjust category importance based on your organization:
- Security-first organizations: Higher security weights
- Fast-moving startups: Emphasize automation
- Enterprise: Balance across all categories

### Custom Questions
Add organization-specific questions:
- Compliance requirements
- Industry-specific practices
- Internal tooling assessments
- Team-specific metrics

## 📞 Support and Troubleshooting

### Common Issues

**Can't access the application**
- Check if services are running: `docker-compose ps`
- Verify ports aren't in use: `lsof -i :8000,:3000`
- Check logs: `docker-compose logs`

**Scores seem wrong**
- Review question responses
- Check scoring weights
- Verify data input accuracy
- Contact support for scoring clarification

**Reports not generating**
- Check browser PDF settings
- Try different browsers
- Verify backend is running
- Check for JavaScript errors

### Getting Help
- Check the FAQ in documentation
- Review GitHub issues
- Contact the development team
- Submit feature requests

## 🎯 Success Stories

### Example: Improving Security Score
**Before**: 45% security score
- No SAST/DAST tools
- Manual security reviews
- No threat modeling

**Actions Taken**:
1. Implemented SonarQube for SAST
2. Added OWASP ZAP to CI/CD
3. Established threat modeling process
4. Regular security training

**After**: 85% security score
- Automated security scanning
- Reduced vulnerabilities by 70%
- Faster security reviews
- Better security awareness

### Example: DevOps Transformation
**Before**: Low DORA metrics
- Monthly deployments
- 2-week lead times
- 4-hour recovery times

**Actions Taken**:
1. Implemented feature flags
2. Automated testing pipeline
3. Added monitoring and alerting
4. Established incident response

**After**: High DORA performance
- Daily deployments
- 2-hour lead times
- 30-minute recovery times

## 🚀 Advanced Features

### API Integration
Integrate StackHealth with your existing tools:
```bash
# Submit scorecard via API
curl -X POST http://localhost:8000/scorecards \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "category": "security", "score": 85}'
```

### Automated Reporting
Schedule regular report generation:
- Weekly team reports
- Monthly executive summaries
- Quarterly trend analysis
- Annual improvement reviews

### Team Dashboards
Create role-specific views:
- **Developers**: Focus on automation and performance
- **Security**: Emphasize security metrics
- **Management**: High-level trends and benchmarks
- **DevOps**: DORA metrics and infrastructure

Start your software quality journey today! 🎉
