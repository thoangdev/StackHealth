// Software Scorecard Dashboard v2.0 - Frontend Application
class ScorecardDashboard {
    constructor() {
        this.baseURL = this.detectBaseURL();
        this.token = localStorage.getItem('authToken');
        this.currentUser = null;
        this.chart = null;
        
        this.init();
    }

    detectBaseURL() {
        // Auto-detect API base URL
        const protocol = window.location.protocol;
        const hostname = window.location.hostname;
        const port = window.location.hostname === 'localhost' ? ':8000' : '';
        return `${protocol}//${hostname}${port}`;
    }

    init() {
        this.setupEventListeners();
        this.setCurrentDate();
        
        if (this.token) {
            this.showDashboard();
            this.loadInitialData();
        } else {
            this.showAuthSection();
        }
    }

    setupEventListeners() {
        // Authentication forms
        document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('registerForm').addEventListener('submit', (e) => this.handleRegister(e));
        
        // Dashboard forms
        document.getElementById('productForm').addEventListener('submit', (e) => this.handleCreateProduct(e));
        document.getElementById('scorecardForm').addEventListener('submit', (e) => this.handleSubmitScorecard(e));
    }

    setCurrentDate() {
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('scorecardDate').value = today;
    }

    // Authentication Methods
    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await axios.post(`${this.baseURL}/auth/login`, {
                email,
                password
            });

            this.token = response.data.access_token;
            localStorage.setItem('authToken', this.token);
            this.setupAxiosDefaults();
            
            this.showAlert('Login successful!', 'success');
            this.showDashboard();
            this.loadInitialData();
        } catch (error) {
            this.showAlert('Login failed: ' + (error.response?.data?.detail || 'Unknown error'), 'error');
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        try {
            await axios.post(`${this.baseURL}/auth/register`, {
                email,
                password
            });

            this.showAlert('Registration successful! Please login.', 'success');
            this.switchAuthTab('login');
        } catch (error) {
            this.showAlert('Registration failed: ' + (error.response?.data?.detail || 'Unknown error'), 'error');
        }
    }

    setupAxiosDefaults() {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
    }

    logout() {
        this.token = null;
        localStorage.removeItem('authToken');
        delete axios.defaults.headers.common['Authorization'];
        
        this.showAuthSection();
        this.showAlert('Logged out successfully!', 'success');
    }

    showAuthSection() {
        document.getElementById('authSection').classList.remove('hidden');
        document.getElementById('dashboard').classList.add('hidden');
    }

    showDashboard() {
        document.getElementById('authSection').classList.add('hidden');
        document.getElementById('dashboard').classList.remove('hidden');
        this.setupAxiosDefaults();
    }

    switchAuthTab(tab) {
        document.querySelectorAll('#authSection .tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('#authSection .tab-content').forEach(t => t.classList.remove('active'));
        
        document.querySelector(`#authSection .tab:nth-child(${tab === 'login' ? 1 : 2})`).classList.add('active');
        document.getElementById(`${tab}Tab`).classList.add('active');
    }

    // Product Management
    async handleCreateProduct(e) {
        e.preventDefault();
        const name = document.getElementById('productName').value;
        const description = document.getElementById('productDescription').value;

        try {
            await axios.post(`${this.baseURL}/products`, {
                name,
                description
            });

            this.showAlert('Product created successfully!', 'success');
            document.getElementById('productForm').reset();
            this.loadProducts();
        } catch (error) {
            this.showAlert('Failed to create product: ' + (error.response?.data?.detail || 'Unknown error'), 'error');
        }
    }

    async loadProducts() {
        try {
            const response = await axios.get(`${this.baseURL}/products`);
            this.displayProducts(response.data);
            this.updateProductSelectors(response.data);
        } catch (error) {
            console.error('Failed to load products:', error);
        }
    }

    displayProducts(products) {
        const container = document.getElementById('productsList');
        
        if (products.length === 0) {
            container.innerHTML = '<p class="loading">No products found. Create your first product above!</p>';
            return;
        }

        container.innerHTML = products.map(product => `
            <div class="scorecard-item">
                <div class="scorecard-header">
                    <h4>${product.name}</h4>
                    <small>Created: ${new Date(product.created_at).toLocaleDateString()}</small>
                </div>
                <p>${product.description || 'No description provided'}</p>
            </div>
        `).join('');
    }

    updateProductSelectors(products) {
        const selectors = ['scorecardProduct', 'trendProduct'];
        
        selectors.forEach(selectorId => {
            const selector = document.getElementById(selectorId);
            selector.innerHTML = '<option value="">Choose a product...</option>';
            
            products.forEach(product => {
                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = product.name;
                selector.appendChild(option);
            });
        });
    }

    // Scorecard Management
    updateScorecardFields() {
        const category = document.getElementById('scorecardCategory').value;
        const container = document.getElementById('scorecardFields');
        
        if (!category) {
            container.innerHTML = '';
            return;
        }

        if (category === 'cicd') {
            this.generateCICDForm(container);
        } else {
            const fields = this.getScorecardFields(category);
            
            container.innerHTML = `
                <div class="form-group">
                    <label><strong>${category.charAt(0).toUpperCase() + category.slice(1)} Assessment Criteria</strong></label>
                    <div class="checkbox-group">
                        ${Object.entries(fields).map(([key, label]) => `
                            <div class="checkbox-item">
                                <input type="checkbox" id="${key}" name="${key}" value="true">
                                <label for="${key}">${label}</label>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    }

    generateCICDForm(container) {
        container.innerHTML = `
            <div class="form-group">
                <label><strong>CI/CD Assessment - DORA Metrics & Process Maturity</strong></label>
                
                <!-- DORA Metrics Section -->
                <div class="dora-metrics-section">
                    <h4>📊 DORA Key Metrics</h4>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="deployment_frequency">Deployment Frequency</label>
                            <select id="deployment_frequency" name="deployment_frequency" required>
                                <option value="">Select frequency...</option>
                                <option value="4">On-demand (multiple deploys per day)</option>
                                <option value="3">Between once per day and once per week</option>
                                <option value="2">Between once per week and once per month</option>
                                <option value="1">Once per month or less frequent</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="lead_time">Lead Time for Changes</label>
                            <select id="lead_time" name="lead_time" required>
                                <option value="">Select lead time...</option>
                                <option value="4">Less than one day</option>
                                <option value="3">Between one day and one week</option>
                                <option value="2">Between one week and one month</option>
                                <option value="1">Longer than one month</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="mttr">Mean Time to Recovery</label>
                            <select id="mttr" name="mttr" required>
                                <option value="">Select recovery time...</option>
                                <option value="4">Less than one hour</option>
                                <option value="3">Less than one day</option>
                                <option value="2">Less than one week</option>
                                <option value="1">Longer than a week</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="change_failure_rate">Change Failure Rate</label>
                            <select id="change_failure_rate" name="change_failure_rate" required>
                                <option value="">Select failure rate...</option>
                                <option value="4">0–15%</option>
                                <option value="2">15–30%</option>
                                <option value="1">More than 30%</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <!-- Core Pipeline Components -->
                <div class="pipeline-section">
                    <h4>🔧 Core Pipeline Components</h4>
                    <div class="checkbox-grid">
                        <div class="checkbox-item">
                            <input type="checkbox" id="automated_builds" name="automated_builds" value="true">
                            <label for="automated_builds">Automated Build Process</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="automated_tests" name="automated_tests" value="true">
                            <label for="automated_tests">Automated Testing in Pipeline</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="code_quality_gates" name="code_quality_gates" value="true">
                            <label for="code_quality_gates">Code Quality Gates & Checks</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="deployment_pipeline" name="deployment_pipeline" value="true">
                            <label for="deployment_pipeline">Standardized Deployment Pipeline</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="rollback_strategy" name="rollback_strategy" value="true">
                            <label for="rollback_strategy">Automated Rollback Strategy</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="environment_parity" name="environment_parity" value="true">
                            <label for="environment_parity">Environment Parity (Dev/Stage/Prod)</label>
                        </div>
                    </div>
                </div>
                
                <!-- Advanced Capabilities -->
                <div class="advanced-section">
                    <h4>🚀 Advanced Capabilities</h4>
                    <div class="checkbox-grid">
                        <div class="checkbox-item">
                            <input type="checkbox" id="infrastructure_as_code" name="infrastructure_as_code" value="true">
                            <label for="infrastructure_as_code">Infrastructure as Code</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="config_management" name="config_management" value="true">
                            <label for="config_management">Configuration Management</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="monitoring_alerts" name="monitoring_alerts" value="true">
                            <label for="monitoring_alerts">Monitoring & Alerting Systems</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="security_integration" name="security_integration" value="true">
                            <label for="security_integration">Security Testing Integration</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="performance_testing_integration" name="performance_testing_integration" value="true">
                            <label for="performance_testing_integration">Performance Testing Integration</label>
                        </div>
                    </div>
                </div>
                
                <!-- Process Maturity -->
                <div class="maturity-section">
                    <h4>⭐ Process Maturity</h4>
                    <div class="checkbox-grid">
                        <div class="checkbox-item">
                            <input type="checkbox" id="feature_flags" name="feature_flags" value="true">
                            <label for="feature_flags">Feature Flags/Toggles</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="blue_green_deployment" name="blue_green_deployment" value="true">
                            <label for="blue_green_deployment">Blue-Green Deployments</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="canary_deployment" name="canary_deployment" value="true">
                            <label for="canary_deployment">Canary Deployments</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="database_migrations" name="database_migrations" value="true">
                            <label for="database_migrations">Automated Database Migrations</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="secrets_management" name="secrets_management" value="true">
                            <label for="secrets_management">Secrets Management</label>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getScorecardFields(category) {
        const fields = {
            security: {
                sast: "Static Application Security Testing (SAST)",
                dast: "Dynamic Application Security Testing (DAST)",
                sast_dast_in_ci: "Security Testing Integrated in CI/CD",
                triaging_findings: "Security Findings Triaged & Remediated",
                secrets_scanning: "Secrets Scanning in CI",
                sca_tool_used: "Software Composition Analysis (SCA) Tool",
                cve_alerts: "Critical CVE Auto-Alerts",
                pr_enforcement: "Dependency Scanning in Pull Requests",
                training: "Developer Security Training",
                threat_modeling: "Threat Modeling Process",
                bug_bounty_policy: "Bug Bounty or Disclosure Policy",
                compliance: "Compliance Standards (SOC2, FedRAMP, etc.)",
                secure_design_reviews: "Security in Design Reviews",
                predeployment_threat_modeling: "Pre-deployment Threat Modeling"
            },
            automation: {
                ci_pipeline: "Continuous Integration Pipeline",
                automated_testing: "Automated Testing Suite",
                deployment_automation: "Automated Deployment Process",
                monitoring_alerts: "Automated Monitoring & Alerts",
                infrastructure_as_code: "Infrastructure as Code"
            },
            performance: {
                load_testing: "Load Testing Implementation",
                performance_monitoring: "Performance Monitoring Tools",
                caching_strategy: "Caching Strategy Implementation",
                database_optimization: "Database Performance Optimization",
                cdn_usage: "Content Delivery Network Usage"
            },
            cicd: {
                // DORA Metrics (Scaled Questions)
                deployment_frequency: "Deployment Frequency",
                lead_time: "Lead Time for Changes", 
                mttr: "Mean Time to Recovery",
                change_failure_rate: "Change Failure Rate",
                
                // Core Pipeline Components (Yes/No)
                automated_builds: "Automated Build Process",
                automated_tests: "Automated Testing in Pipeline",
                code_quality_gates: "Code Quality Gates & Checks",
                deployment_pipeline: "Standardized Deployment Pipeline",
                rollback_strategy: "Automated Rollback Strategy",
                environment_parity: "Environment Parity (Dev/Stage/Prod)",
                
                // Advanced Capabilities (Yes/No)
                infrastructure_as_code: "Infrastructure as Code",
                config_management: "Configuration Management",
                monitoring_alerts: "Monitoring & Alerting Systems",
                security_integration: "Security Testing Integration",
                performance_testing_integration: "Performance Testing Integration",
                
                // Process Maturity (Yes/No)
                feature_flags: "Feature Flags/Toggles",
                blue_green_deployment: "Blue-Green Deployments",
                canary_deployment: "Canary Deployments",
                database_migrations: "Automated Database Migrations",
                secrets_management: "Secrets Management"
            }
        };

        return fields[category] || {};
    }

    async handleSubmitScorecard(e) {
        e.preventDefault();
        
        const productId = parseInt(document.getElementById('scorecardProduct').value);
        const category = document.getElementById('scorecardCategory').value;
        const date = document.getElementById('scorecardDate').value;
        
        // Collect values based on category
        const breakdown = {};
        
        if (category === 'cicd') {
            // Collect DORA metrics (select values)
            const doraMetrics = ['deployment_frequency', 'lead_time', 'mttr', 'change_failure_rate'];
            doraMetrics.forEach(metric => {
                const select = document.getElementById(metric);
                breakdown[metric] = select ? parseInt(select.value) || 0 : 0;
            });
            
            // Collect yes/no capabilities (checkboxes)
            const capabilities = [
                'automated_builds', 'automated_tests', 'code_quality_gates', 'deployment_pipeline',
                'rollback_strategy', 'environment_parity', 'infrastructure_as_code', 'config_management',
                'monitoring_alerts', 'security_integration', 'performance_testing_integration',
                'feature_flags', 'blue_green_deployment', 'canary_deployment', 'database_migrations',
                'secrets_management'
            ];
            capabilities.forEach(capability => {
                const checkbox = document.getElementById(capability);
                breakdown[capability] = checkbox ? checkbox.checked : false;
            });
        } else {
            // Standard checkbox collection for other categories
            const fields = this.getScorecardFields(category);
            Object.keys(fields).forEach(field => {
                const checkbox = document.getElementById(field);
                breakdown[field] = checkbox ? checkbox.checked : false;
            });
        }

        try {
            await axios.post(`${this.baseURL}/scorecards`, {
                product_id: productId,
                category,
                date,
                breakdown
            });

            this.showAlert('Scorecard submitted successfully!', 'success');
            document.getElementById('scorecardForm').reset();
            document.getElementById('scorecardFields').innerHTML = '';
            this.loadScorecards();
        } catch (error) {
            this.showAlert('Failed to submit scorecard: ' + (error.response?.data?.detail || 'Unknown error'), 'error');
        }
    }

    async loadScorecards() {
        try {
            const response = await axios.get(`${this.baseURL}/scorecards`);
            this.displayScorecards(response.data);
        } catch (error) {
            console.error('Failed to load scorecards:', error);
        }
    }

    displayScorecards(scorecards) {
        const container = document.getElementById('scorecardsList');
        
        if (scorecards.length === 0) {
            container.innerHTML = '<p class="loading">No scorecards found. Submit your first scorecard!</p>';
            return;
        }

        container.innerHTML = scorecards.map(scorecard => `
            <div class="scorecard-item">
                <div class="scorecard-header">
                    <div>
                        <h4>${scorecard.product_name} - ${scorecard.category.charAt(0).toUpperCase() + scorecard.category.slice(1)}</h4>
                        <small>Date: ${new Date(scorecard.date).toLocaleDateString()}</small>
                    </div>
                    <div>
                        <span class="score-badge ${this.getScoreClass(scorecard.score)}">
                            ${scorecard.score.toFixed(1)}%
                        </span>
                        <button class="btn btn-secondary" onclick="dashboard.downloadPDF(${scorecard.id})">
                            <i class="fas fa-download"></i> PDF
                        </button>
                    </div>
                </div>
                <div style="margin-top: 15px;">
                    <h5>Feedback:</h5>
                    <p>${scorecard.feedback || 'No feedback available'}</p>
                </div>
                ${scorecard.tool_suggestions ? `
                    <div style="margin-top: 10px;">
                        <h5>Recommended Tools:</h5>
                        <p>${scorecard.tool_suggestions}</p>
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    getScoreClass(score) {
        if (score >= 80) return 'score-excellent';
        if (score >= 60) return 'score-good';
        if (score >= 40) return 'score-fair';
        return 'score-poor';
    }

    async downloadPDF(scorecardId) {
        try {
            const response = await axios.get(`${this.baseURL}/scorecards/${scorecardId}/pdf`, {
                responseType: 'blob'
            });

            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scorecard_${scorecardId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            this.showAlert('Failed to download PDF: ' + (error.response?.data?.detail || 'Unknown error'), 'error');
        }
    }

    // Trends and Analytics
    async loadTrends() {
        const productId = document.getElementById('trendProduct').value;
        const category = document.getElementById('trendCategory').value;
        
        if (!productId || !category) {
            return;
        }

        try {
            const response = await axios.get(`${this.baseURL}/trends/${productId}/${category}?days=90`);
            this.displayTrendChart(response.data, category);
        } catch (error) {
            console.error('Failed to load trends:', error);
        }
    }

    displayTrendChart(data, category) {
        const ctx = document.getElementById('trendChart').getContext('2d');
        
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = data.map(item => new Date(item.date).toLocaleDateString());
        const scores = data.map(item => item.score);

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: `${category.charAt(0).toUpperCase() + category.slice(1)} Score`,
                    data: scores,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: `${category.charAt(0).toUpperCase() + category.slice(1)} Score Trends`
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Score (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }

    // UI Helper Methods
    switchTab(tabName) {
        document.querySelectorAll('#dashboard .tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('#dashboard .tab-content').forEach(content => content.classList.remove('active'));
        
        event.target.classList.add('active');
        document.getElementById(`${tabName}Tab`).classList.add('active');
        
        // Load data when switching to certain tabs
        if (tabName === 'reports') {
            this.loadScorecards();
        }
    }

    showAlert(message, type = 'success') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        
        // Insert after header
        const header = document.querySelector('.header');
        header.insertAdjacentElement('afterend', alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    async loadInitialData() {
        try {
            await this.loadProducts();
            await this.loadScorecards();
        } catch (error) {
            console.error('Failed to load initial data:', error);
        }
    }
}

// Global functions for HTML onclick handlers
function switchTab(tabName) {
    dashboard.switchTab(tabName);
}

function switchAuthTab(tabName) {
    dashboard.switchAuthTab(tabName);
}

function updateScorecardFields() {
    dashboard.updateScorecardFields();
}

function loadTrends() {
    dashboard.loadTrends();
}

function logout() {
    dashboard.logout();
}

// Initialize the dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new ScorecardDashboard();
});
