from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import date
import database
import schemas
import json


def create_product(db: Session, product: schemas.ProductCreate) -> database.Product:
    """Create a new product"""
    db_product = database.Product(
        name=product.name,
        description=product.description
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[database.Product]:
    """Get all products ordered by creation date (newest first)"""
    return db.query(database.Product).order_by(database.Product.created_at.desc()).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int) -> Optional[database.Product]:
    """Get a product by ID"""
    return db.query(database.Product).filter(database.Product.id == product_id).first()


def get_product_by_name(db: Session, name: str) -> Optional[database.Product]:
    """Get a product by name"""
    return db.query(database.Product).filter(database.Product.name == name).first()


def calculate_score(breakdown: Dict[str, Any], category: str) -> float:
    """Calculate category score as percentage (0-100%) based on breakdown fields"""
    
    # Updated weights for independent category scoring
    weights = {
        "security": {
            # Static & Dynamic Testing (12 points = 40%)
            "sast": 3, "dast": 3, "sast_dast_in_ci": 4, "triaging_findings": 2,
            # Dependency & Secrets Management (8 points = 27%)
            "secrets_scanning": 2, "sca_tool_used": 3, "cve_alerts": 3,
            # Security Culture & Governance (10 points = 33%)
            "threat_modeling": 3, "compliance": 2, "training": 2, 
            "bug_bounty_policy": 1, "security_champions": 2
        },
        "automation": {
            # Test Automation Foundation (15 points = 37.5%)
            "automated_testing": 2, "testing_framework": 3, "dedicated_environment": 2,
            "source_controlled": 3, "quick_setup": 1, "external_updates": 2, "test_reporting": 2,
            # Test Design & Maintenance (13 points = 32.5%)
            "seeded_data": 2, "test_independence": -5, "data_reseeding": 3,
            "test_subsets": 3, "rapid_updates": 2, "database_automation": 2,
            "cross_browser_testing": 2, "parallel_execution": 2, "flakiness_management": 2,
            # CI/CD Integration & Deployment Testing (12 points = 30%)
            "post_deploy_sanity": 3, "sanity_independence": -2, "smoke_testing": 3,
            "performance_integration": 2, "security_integration": 2, "notification_integration": 1,
            "test_dashboard": 2, "automated_scheduling": 1
        },
        "performance": {
            # Performance Strategy & Planning (10 points = 33%)
            "performance_requirements": 3, "regular_testing": 2, "performance_budget": 2, "trend_analysis": 3,
            # Testing Implementation & Tools (12 points = 40%)
            "dedicated_tools": 2, "ci_integration": 4, "production_like_env": 3, "load_testing": 3,
            # Monitoring & Observability (8 points = 27%)
            "realtime_monitoring": 2, "core_metrics": 2, "resource_utilization": 1,
            "dashboard_viz": 2, "automated_alerting": 1
        },
        "cicd": {
            # DORA Metrics (20 points = 44%)
            "deployment_frequency": 5, "lead_time": 5, "recovery_time": 5, "change_failure_rate": 5,
            # Pipeline Foundation (15 points = 33%)
            "automated_builds": 3, "automated_tests": 4, "code_quality_gates": 3,
            "security_integration": 3, "artifact_management": 2,
            # Deployment & Release Management (10 points = 23%)
            "automated_deployment": 3, "environment_promotion": 2, "rollback_capability": 3,
            "feature_flags": 2
        }
    }
    
    category_weights = weights.get(category, {})
    total_weighted_score = 0
    total_possible_score = 0
    
    # Calculate maximum possible score for the category
    max_scores = {
        "security": 30,
        "automation": 40,  # Base score, bonuses can exceed this
        "performance": 30,
        "cicd": 45  # Base score, bonuses can exceed this
    }
    
    category_max = max_scores.get(category, 100)
    
    # Special handling for different field types
    dora_metrics = ['deployment_frequency', 'lead_time', 'recovery_time', 'change_failure_rate']
    coverage_fields = ['api_coverage', 'functional_coverage', 'integration_coverage', 'workflow_coverage']
    test_type_fields = ['test_types', 'load_testing']
    
    for field, value in breakdown.items():
        weight = category_weights.get(field, 0)
        
        if weight == 0:
            continue  # Skip fields not in weights
        
        if category == "cicd" and field in dora_metrics:
            # DORA metrics: map string values to scores
            dora_scores = {
                "on-demand": 5, "daily": 4, "weekly": 2, "monthly": 1,
                "<1hour": 5, "<1day": 4, "<1week": 2, ">1week": 1,
                "0-5%": 5, "6-15%": 4, "16-30%": 2, ">30%": 1
            }
            score_value = dora_scores.get(value, 0)
            total_weighted_score += score_value
            total_possible_score += 5  # Max DORA score
            
        elif field in coverage_fields:
            # Coverage fields: map percentage ranges to scores
            if field == "api_coverage":
                coverage_scores = {"0%": 0, "1-20%": 1, "20-40%": 2, 
                                 "40-60%": 4, "60-80%": 7, "80-100%": 10}
                max_score = 10  # Bonus points
            elif field == "functional_coverage":
                coverage_scores = {"0%": 0, "1-20%": 1, "20-40%": 2, 
                                 "40-70%": 3, "70-100%": 5}
                max_score = 5  # Bonus points
            elif field == "integration_coverage":
                coverage_scores = {"0%": 0, "1-50%": 1, "50-80%": 2, "80-100%": 3}
                max_score = 3  # Bonus points
            else:  # workflow_coverage
                coverage_scores = {"0%": 0, "1-20%": 1, "20-50%": 2, "50-100%": 4}
                max_score = 4
            
            score_value = coverage_scores.get(value, 0)
            total_weighted_score += score_value
            # For automation bonuses, don't add to total_possible_score
            if category != "automation":
                total_possible_score += max_score
                
        elif field in test_type_fields:
            if field == "test_types":
                # Performance test types
                type_scores = {"smoke": 1, "load": 2, "stress": 3, "spike": 4, "soak": 5}
                score_value = type_scores.get(value, 0)
                total_weighted_score += score_value
                total_possible_score += 5
            elif field == "load_testing":
                # CI/CD load testing integration
                total_weighted_score += (1 if value else 0) * weight
                total_possible_score += weight
            
        else:
            # Boolean fields with potential negative weights (anti-patterns)
            if weight < 0:
                # For negative weights (anti-patterns)
                if not value:  # Anti-pattern is present (field is False)
                    total_weighted_score += weight  # Add penalty
                # If value is True, no penalty applied
                total_possible_score += abs(weight)
            else:
                # Normal positive scoring
                total_weighted_score += (1 if value else 0) * weight
                total_possible_score += weight
    
    # Calculate percentage score
    if total_possible_score == 0:
        return 0.0
    
    # For categories with bonuses (automation, cicd), allow scores > 100%
    percentage_score = (total_weighted_score / category_max) * 100
    
    # Ensure score doesn't go below 0 due to penalties
    final_score = max(0, percentage_score)
    
    return round(final_score, 2)


def generate_feedback_and_suggestions(breakdown: Dict[str, Any], category: str, score: float) -> tuple[str, str]:
    """Generate feedback and tool suggestions based on scorecard results"""
    feedback_lines = []
    suggestions = []
    
    if category == "security":
        if not breakdown.get("sast", False):
            feedback_lines.append("❌ No Static Application Security Testing (SAST) in place")
            suggestions.append("Consider tools like SonarQube, Checkmarx, or Veracode")
        if not breakdown.get("dast", False):
            feedback_lines.append("❌ No Dynamic Application Security Testing (DAST) in place")
            suggestions.append("Consider OWASP ZAP, Burp Suite, or Rapid7")
        if not breakdown.get("sast_dast_in_ci", False):
            feedback_lines.append("❌ Security testing not integrated into CI/CD pipeline")
            suggestions.append("Integrate security scans into your CI/CD pipeline")
        if not breakdown.get("secrets_scanning", False):
            feedback_lines.append("❌ No secrets scanning in place")
            suggestions.append("Use GitLeaks, TruffleHog, or GitHub Secret Scanning")
        if not breakdown.get("sca_tool_used", False):
            feedback_lines.append("❌ No Software Composition Analysis (SCA) tool")
            suggestions.append("Consider Snyk, FOSSA, or WhiteSource")
    
    elif category == "automation":
        if not breakdown.get("ci_pipeline", False):
            feedback_lines.append("❌ No CI pipeline implementation")
            suggestions.append("Implement GitHub Actions, GitLab CI, or Jenkins")
        if not breakdown.get("automated_testing", False):
            feedback_lines.append("❌ Limited automated testing")
            suggestions.append("Implement unit, integration, and e2e tests")
        if not breakdown.get("deployment_automation", False):
            feedback_lines.append("❌ Manual deployment processes")
            suggestions.append("Consider Terraform, Ansible, or Kubernetes")
    
    elif category == "performance":
        if not breakdown.get("performance_monitoring", False):
            feedback_lines.append("❌ No performance monitoring in place")
            suggestions.append("Implement APM tools like New Relic, Datadog, or Prometheus")
        if not breakdown.get("load_testing", False):
            feedback_lines.append("❌ No load testing practices")
            suggestions.append("Use k6, JMeter, or Artillery for load testing")
    
    elif category == "cicd":
        # DORA Metrics Analysis
        deployment_freq = breakdown.get("deployment_frequency", 0)
        if deployment_freq == 1:
            feedback_lines.append("❌ Low deployment frequency (monthly or less)")
            suggestions.append("Implement feature flags and smaller batch sizes for more frequent deployments")
        elif deployment_freq == 2:
            feedback_lines.append("⚠️ Moderate deployment frequency (weekly-monthly)")
            suggestions.append("Consider daily deployments with automated testing")
        
        lead_time = breakdown.get("lead_time", 0)
        if lead_time <= 2:
            feedback_lines.append("❌ Long lead time for changes (week+ to month+)")
            suggestions.append("Streamline your development workflow and reduce batch sizes")
        
        mttr = breakdown.get("mttr", 0)
        if mttr <= 2:
            feedback_lines.append("❌ Slow recovery time (day+ to week+)")
            suggestions.append("Implement better monitoring, alerting, and incident response procedures")
        
        change_failure = breakdown.get("change_failure_rate", 0)
        if change_failure == 1:
            feedback_lines.append("❌ High change failure rate (30%+)")
            suggestions.append("Improve testing practices and implement gradual rollouts")
        
        # Core Pipeline Issues
        if not breakdown.get("automated_builds", False):
            feedback_lines.append("❌ No automated build process")
            suggestions.append("Set up automated builds with GitHub Actions, GitLab CI, or Jenkins")
        if not breakdown.get("automated_tests", False):
            feedback_lines.append("❌ No automated testing in pipeline")
            suggestions.append("Integrate unit, integration, and e2e tests into CI/CD")
        if not breakdown.get("deployment_pipeline", False):
            feedback_lines.append("❌ No standardized deployment pipeline")
            suggestions.append("Create consistent deployment pipelines across environments")
        if not breakdown.get("rollback_strategy", False):
            feedback_lines.append("❌ No rollback strategy")
            suggestions.append("Implement automated rollback capabilities")
        
        # Advanced Capabilities
        if not breakdown.get("infrastructure_as_code", False):
            suggestions.append("Consider Infrastructure as Code with Terraform or CloudFormation")
        if not breakdown.get("security_integration", False):
            suggestions.append("Integrate security scanning into your CI/CD pipeline")
        if not breakdown.get("monitoring_alerts", False):
            suggestions.append("Set up comprehensive monitoring and alerting systems")
    
    # Add positive feedback for good scores
    if score >= 80:
        feedback_lines.insert(0, "✅ Excellent scorecard performance!")
    elif score >= 60:
        feedback_lines.insert(0, "✅ Good progress with room for improvement")
    else:
        feedback_lines.insert(0, "⚠️ Significant improvements needed")
    
    feedback = "\n".join(feedback_lines) if feedback_lines else "Great job on all metrics!"
    tool_suggestions = "\n".join(f"• {suggestion}" for suggestion in suggestions)
    
    return feedback, tool_suggestions


def create_scorecard(
    db: Session, 
    scorecard: schemas.ScorecardCreate
) -> database.Scorecard:
    """Create a scorecard with calculated score and feedback"""
    
    # Convert breakdown to dict
    breakdown_dict = scorecard.breakdown.dict()
    
    # Calculate overall score
    calculated_score = calculate_score(breakdown_dict, scorecard.category)
    
    # Generate feedback and suggestions
    feedback, tool_suggestions = generate_feedback_and_suggestions(
        breakdown_dict, scorecard.category, calculated_score
    )
    
    # Create the scorecard
    db_scorecard = database.Scorecard(
        product_id=scorecard.product_id,
        category=scorecard.category,
        date=scorecard.date,
        score=calculated_score,
        breakdown=breakdown_dict,
        feedback=feedback,
        tool_suggestions=tool_suggestions
    )
    db.add(db_scorecard)
    db.commit()
    db.refresh(db_scorecard)
    return db_scorecard


def get_scorecards_by_product(
    db: Session, 
    product_id: Optional[int] = None, 
    category: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[database.Scorecard]:
    """Get scorecards, optionally filtered by product and category"""
    query = db.query(database.Scorecard)
    
    if product_id:
        query = query.filter(database.Scorecard.product_id == product_id)
    if category:
        query = query.filter(database.Scorecard.category == category)
    
    return query.order_by(database.Scorecard.date.desc()).offset(skip).limit(limit).all()


def get_scorecard_by_id(db: Session, scorecard_id: int) -> Optional[database.Scorecard]:
    """Get a scorecard by ID"""
    return db.query(database.Scorecard).filter(database.Scorecard.id == scorecard_id).first()


def get_trend_data(
    db: Session, 
    product_id: int, 
    category: str, 
    quarters: int = 4
) -> List[database.Scorecard]:
    """Get quarterly trend data for a product's specific category over time"""
    from datetime import datetime, timedelta
    
    # Calculate start date based on quarters (each quarter = 3 months)
    months_back = quarters * 3
    start_date = datetime.now().date() - timedelta(days=months_back * 30)  # Approximate
    
    return db.query(database.Scorecard).filter(
        database.Scorecard.product_id == product_id,
        database.Scorecard.category == category,
        database.Scorecard.date >= start_date
    ).order_by(database.Scorecard.date.asc()).all()


def get_quarterly_improvement_data(
    db: Session,
    product_id: int,
    category: str
) -> List[database.Scorecard]:
    """Get quarterly assessment data showing improvement trends"""
    from datetime import datetime, timedelta
    
    # Get last 12 months of data to show quarterly progression
    start_date = datetime.now().date() - timedelta(days=365)
    
    scorecards = db.query(database.Scorecard).filter(
        database.Scorecard.product_id == product_id,
        database.Scorecard.category == category,
        database.Scorecard.date >= start_date
    ).order_by(database.Scorecard.date.asc()).all()
    
    # Group by quarters and return the most recent scorecard per quarter
    quarterly_data = {}
    for scorecard in scorecards:
        quarter_key = f"{scorecard.date.year}-Q{((scorecard.date.month - 1) // 3) + 1}"
        if quarter_key not in quarterly_data or scorecard.date > quarterly_data[quarter_key].date:
            quarterly_data[quarter_key] = scorecard
    
    return list(quarterly_data.values())
