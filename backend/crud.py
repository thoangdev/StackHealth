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
    """Get all products"""
    return db.query(database.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int) -> Optional[database.Product]:
    """Get a product by ID"""
    return db.query(database.Product).filter(database.Product.id == product_id).first()


def get_product_by_name(db: Session, name: str) -> Optional[database.Product]:
    """Get a product by name"""
    return db.query(database.Product).filter(database.Product.name == name).first()


def calculate_score(breakdown: Dict[str, Any], category: str) -> float:
    """Calculate overall score based on breakdown fields"""
    weights = {
        "security": {
            "sast": 2, "dast": 2, "sast_dast_in_ci": 3, "triaging_findings": 2, 
            "secrets_scanning": 1, "sca_tool_used": 2, "cve_alerts": 2, 
            "pr_enforcement": 2, "training": 1, "threat_modeling": 2, 
            "bug_bounty_policy": 1, "compliance": 1, "secure_design_reviews": 2, 
            "predeployment_threat_modeling": 2
        },
        "automation": {
            "ci_pipeline": 3, "automated_testing": 3, "deployment_automation": 2,
            "monitoring_alerts": 1, "infrastructure_as_code": 1
        },
        "performance": {
            "load_testing": 2, "performance_monitoring": 3, "caching_strategy": 1,
            "database_optimization": 2, "cdn_usage": 1
        },
        "cicd": {
            # DORA Metrics (Core Performance)
            "deployment_frequency": 4, "lead_time": 4, "mttr": 4, "change_failure_rate": 4,
            
            # Core Pipeline Components
            "automated_builds": 3, "automated_tests": 4, "code_quality_gates": 2,
            "deployment_pipeline": 3, "rollback_strategy": 2, "environment_parity": 2,
            
            # Advanced Capabilities
            "infrastructure_as_code": 2, "config_management": 2, "monitoring_alerts": 2,
            "security_integration": 3, "performance_testing_integration": 2,
            
            # Process Maturity
            "feature_flags": 1, "blue_green_deployment": 1, "canary_deployment": 1,
            "database_migrations": 1, "secrets_management": 2
        }
    }
    
    category_weights = weights.get(category, {})
    total_weighted_score = 0
    total_possible_score = 0
    
    # Special handling for CI/CD DORA metrics (scaled 1-4) vs boolean fields
    dora_metrics = ['deployment_frequency', 'lead_time', 'mttr', 'change_failure_rate']
    
    for field, value in breakdown.items():
        weight = category_weights.get(field, 1)
        
        if category == "cicd" and field in dora_metrics:
            # DORA metrics are scaled 1-4, normalize to 0-1
            normalized_value = max(0, int(value) - 1) / 3  # Convert 1-4 to 0-1
            total_weighted_score += normalized_value * weight
        else:
            # Boolean fields: 1 if True, 0 if False
            total_weighted_score += (1 if value else 0) * weight
        
        total_possible_score += weight
    
    if total_possible_score == 0:
        return 0.0
    
    return round((total_weighted_score / total_possible_score) * 100, 2)


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
    days: int = 30
) -> List[database.Scorecard]:
    """Get trend data for a product's specific category over time"""
    from datetime import datetime, timedelta
    
    start_date = datetime.now().date() - timedelta(days=days)
    
    return db.query(database.Scorecard).filter(
        database.Scorecard.product_id == product_id,
        database.Scorecard.category == category,
        database.Scorecard.date >= start_date
    ).order_by(database.Scorecard.date.asc()).all()
