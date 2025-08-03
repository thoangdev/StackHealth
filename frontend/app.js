// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : '/api';

// Global state
let projects = [];
let scorecards = [];
let trendChart = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeDateInput();
    loadProjects();
    loadScorecards();
    setupEventListeners();
});

// Set default date to today
function initializeDateInput() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('scorecardDate').value = today;
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('scorecardForm').addEventListener('submit', handleScorecardSubmit);
    document.getElementById('projectForm').addEventListener('submit', handleProjectSubmit);
    document.getElementById('filterProject').addEventListener('change', handleProjectFilter);
}

// Tab switching functionality
function showTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab content
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked tab
    event.target.classList.add('active');
    
    // Load data when switching to certain tabs
    if (tabName === 'view') {
        loadScorecards();
    } else if (tabName === 'projects') {
        loadProjects();
    }
}

// API Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        const response = await axios({
            method,
            url: `${API_BASE_URL}${endpoint}`,
            data,
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Load projects from API
async function loadProjects() {
    try {
        projects = await apiCall('/projects');
        updateProjectSelects();
        updateProjectsList();
    } catch (error) {
        showAlert('projectAlert', 'Error loading projects', 'error');
    }
}

// Update project dropdown options
function updateProjectSelects() {
    const projectSelect = document.getElementById('projectSelect');
    const filterSelect = document.getElementById('filterProject');
    
    // Clear existing options (except first)
    projectSelect.innerHTML = '<option value="">Select a project...</option>';
    filterSelect.innerHTML = '<option value="">All projects</option>';
    
    // Add project options
    projects.forEach(project => {
        const option1 = new Option(project.name, project.id);
        const option2 = new Option(project.name, project.id);
        projectSelect.appendChild(option1);
        filterSelect.appendChild(option2);
    });
}

// Handle project form submission
async function handleProjectSubmit(event) {
    event.preventDefault();
    
    const projectData = {
        name: document.getElementById('projectName').value.trim(),
        description: document.getElementById('projectDescription').value.trim() || null
    };
    
    try {
        await apiCall('/projects', 'POST', projectData);
        showAlert('projectAlert', 'Project created successfully!', 'success');
        document.getElementById('projectForm').reset();
        loadProjects();
    } catch (error) {
        const message = error.response?.data?.detail || 'Error creating project';
        showAlert('projectAlert', message, 'error');
    }
}

// Handle scorecard form submission
async function handleScorecardSubmit(event) {
    event.preventDefault();
    
    const feedback = [];
    const areas = ['automation', 'performance', 'security', 'cicd'];
    
    // Collect feedback for each area
    areas.forEach(area => {
        const comment = document.getElementById(`${area}Feedback`).value.trim();
        const tools = document.getElementById(`${area}Tools`).value.trim();
        const improvement = document.getElementById(`${area}Improvement`).checked;
        
        if (comment || tools || improvement) {
            feedback.push({
                area,
                comment: comment || null,
                tool_recommendation: tools || null,
                marked_for_improvement: improvement
            });
        }
    });
    
    const scorecardData = {
        project_id: parseInt(document.getElementById('projectSelect').value),
        date: document.getElementById('scorecardDate').value,
        automation_score: parseFloat(document.getElementById('automationScore').value),
        performance_score: parseFloat(document.getElementById('performanceScore').value),
        security_score: parseFloat(document.getElementById('securityScore').value),
        cicd_score: parseFloat(document.getElementById('cicdScore').value),
        feedback
    };
    
    try {
        await apiCall('/scorecards', 'POST', scorecardData);
        showAlert('submitAlert', 'Scorecard submitted successfully!', 'success');
        document.getElementById('scorecardForm').reset();
        initializeDateInput();
        loadScorecards();
    } catch (error) {
        const message = error.response?.data?.detail || 'Error submitting scorecard';
        showAlert('submitAlert', message, 'error');
    }
}

// Load scorecards from API
async function loadScorecards() {
    try {
        document.getElementById('scorecardsLoading').style.display = 'block';
        
        const projectId = document.getElementById('filterProject')?.value;
        const endpoint = projectId ? `/scorecards?project_id=${projectId}` : '/scorecards';
        
        scorecards = await apiCall(endpoint);
        updateScorecardsTable();
        updateTrendChart();
        
        document.getElementById('scorecardsLoading').style.display = 'none';
    } catch (error) {
        document.getElementById('scorecardsLoading').innerHTML = 'Error loading scorecards';
    }
}

// Handle project filter change
function handleProjectFilter() {
    loadScorecards();
}

// Update scorecards table
function updateScorecardsTable() {
    const container = document.getElementById('scorecardsContainer');
    
    if (scorecards.length === 0) {
        container.innerHTML = '<p>No scorecards found.</p>';
        return;
    }
    
    const table = document.createElement('table');
    table.className = 'scorecard-table';
    
    // Table header
    table.innerHTML = `
        <thead>
            <tr>
                <th>Project</th>
                <th>Date</th>
                <th>Automation</th>
                <th>Performance</th>
                <th>Security</th>
                <th>CI/CD</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            ${scorecards.map(scorecard => `
                <tr>
                    <td>${scorecard.project_name}</td>
                    <td>${formatDate(scorecard.date)}</td>
                    <td>${getScoreBadge(scorecard.automation_score)}</td>
                    <td>${getScoreBadge(scorecard.performance_score)}</td>
                    <td>${getScoreBadge(scorecard.security_score)}</td>
                    <td>${getScoreBadge(scorecard.cicd_score)}</td>
                    <td>
                        <button class="btn btn-secondary" onclick="downloadPDF(${scorecard.id})">
                            📄 Export PDF
                        </button>
                    </td>
                </tr>
            `).join('')}
        </tbody>
    `;
    
    container.innerHTML = '';
    container.appendChild(table);
}

// Update projects list
function updateProjectsList() {
    const container = document.getElementById('projectsList');
    document.getElementById('projectsLoading').style.display = 'none';
    
    if (projects.length === 0) {
        container.innerHTML = '<p>No projects found.</p>';
        return;
    }
    
    const projectsHtml = projects.map(project => `
        <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 20px; margin-bottom: 15px; background: white;">
            <h4 style="margin-bottom: 10px; color: #333;">${project.name}</h4>
            ${project.description ? `<p style="color: #666; margin-bottom: 10px;">${project.description}</p>` : ''}
            <small style="color: #999;">Created: ${formatDate(project.created_at)}</small>
        </div>
    `).join('');
    
    container.innerHTML = projectsHtml;
}

// Update trend chart
function updateTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    // Destroy existing chart
    if (trendChart) {
        trendChart.destroy();
    }
    
    // Prepare data for chart
    const chartData = prepareTrendData();
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: 'Automation',
                    data: chartData.automation,
                    borderColor: '#ff6384',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.1
                },
                {
                    label: 'Performance',
                    data: chartData.performance,
                    borderColor: '#36a2eb',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.1
                },
                {
                    label: 'Security',
                    data: chartData.security,
                    borderColor: '#ffce56',
                    backgroundColor: 'rgba(255, 206, 86, 0.1)',
                    tension: 0.1
                },
                {
                    label: 'CI/CD',
                    data: chartData.cicd,
                    borderColor: '#4bc0c0',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
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
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Score Trends Over Time'
                },
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

// Prepare data for trend chart
function prepareTrendData() {
    // Sort scorecards by date
    const sortedScorecards = [...scorecards].sort((a, b) => new Date(a.date) - new Date(b.date));
    
    return {
        labels: sortedScorecards.map(s => formatDate(s.date)),
        automation: sortedScorecards.map(s => s.automation_score),
        performance: sortedScorecards.map(s => s.performance_score),
        security: sortedScorecards.map(s => s.security_score),
        cicd: sortedScorecards.map(s => s.cicd_score)
    };
}

// Download PDF for a scorecard
async function downloadPDF(scorecardId) {
    try {
        const response = await axios({
            method: 'GET',
            url: `${API_BASE_URL}/scorecards/${scorecardId}/pdf`,
            responseType: 'blob'
        });
        
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        
        // Get filename from response headers or generate one
        const contentDisposition = response.headers['content-disposition'];
        let filename = `scorecard_${scorecardId}.pdf`;
        if (contentDisposition) {
            const matches = /filename="([^"]*)"/.exec(contentDisposition);
            if (matches) filename = matches[1];
        }
        
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        alert('Error downloading PDF');
    }
}

// Utility functions
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString();
}

function getScoreBadge(score) {
    let className = 'score-low';
    if (score >= 80) className = 'score-high';
    else if (score >= 60) className = 'score-medium';
    
    return `<span class="score-badge ${className}">${score}%</span>`;
}

function showAlert(containerId, message, type) {
    const container = document.getElementById(containerId);
    const className = type === 'success' ? 'alert-success' : 'alert-error';
    
    container.innerHTML = `<div class="alert ${className}">${message}</div>`;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}
