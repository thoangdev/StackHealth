from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import database
import schemas


def create_project(db: Session, project: schemas.ProjectCreate) -> database.Project:
    """Create a new project"""
    db_project = database.Project(
        name=project.name,
        description=project.description
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[database.Project]:
    """Get all projects"""
    return db.query(database.Project).offset(skip).limit(limit).all()


def get_project_by_id(db: Session, project_id: int) -> Optional[database.Project]:
    """Get a project by ID"""
    return db.query(database.Project).filter(database.Project.id == project_id).first()


def get_project_by_name(db: Session, name: str) -> Optional[database.Project]:
    """Get a project by name"""
    return db.query(database.Project).filter(database.Project.name == name).first()


def create_scorecard_with_feedback(
    db: Session, 
    scorecard: schemas.ScorecardCreate
) -> database.Scorecard:
    """Create a scorecard with associated feedback"""
    
    # Create the scorecard
    db_scorecard = database.Scorecard(
        project_id=scorecard.project_id,
        date=scorecard.date,
        automation_score=scorecard.automation_score,
        performance_score=scorecard.performance_score,
        security_score=scorecard.security_score,
        cicd_score=scorecard.cicd_score
    )
    db.add(db_scorecard)
    db.flush()  # Flush to get the ID without committing
    
    # Add auto-recommendations for scores < 70
    auto_feedback = []
    tool_recommendations = {
        "automation": "Playwright, Selenium, Cypress",
        "performance": "k6, JMeter, Lighthouse",
        "security": "OWASP ZAP, SonarQube, Snyk",
        "cicd": "GitHub Actions, Jenkins, GitLab CI"
    }
    
    scores = {
        "automation": scorecard.automation_score,
        "performance": scorecard.performance_score,
        "security": scorecard.security_score,
        "cicd": scorecard.cicd_score
    }
    
    # Add auto-recommendations for low scores
    for area, score in scores.items():
        if score < 70:
            auto_feedback.append(schemas.FeedbackCreate(
                area=area,
                comment=f"Score below 70% - consider improvements",
                tool_recommendation=tool_recommendations[area],
                marked_for_improvement=True
            ))
    
    # Combine user feedback with auto-generated feedback
    all_feedback = (scorecard.feedback or []) + auto_feedback
    
    # Create feedback entries
    for feedback_data in all_feedback:
        db_feedback = database.Feedback(
            scorecard_id=db_scorecard.id,
            area=feedback_data.area,
            comment=feedback_data.comment,
            tool_recommendation=feedback_data.tool_recommendation,
            marked_for_improvement=feedback_data.marked_for_improvement
        )
        db.add(db_feedback)
    
    db.commit()
    db.refresh(db_scorecard)
    return db_scorecard


def get_scorecards_by_project(
    db: Session, 
    project_id: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[database.Scorecard]:
    """Get scorecards, optionally filtered by project"""
    query = db.query(database.Scorecard)
    if project_id:
        query = query.filter(database.Scorecard.project_id == project_id)
    return query.order_by(database.Scorecard.date.desc()).offset(skip).limit(limit).all()


def get_scorecard_by_id(db: Session, scorecard_id: int) -> Optional[database.Scorecard]:
    """Get a scorecard by ID with all related data"""
    return db.query(database.Scorecard).filter(database.Scorecard.id == scorecard_id).first()
