from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import crud
import schemas
import database
from pdf_generator import generate_pdf_report

app = FastAPI(
    title="Software Scorecard Dashboard API",
    description="API for tracking and visualizing software scorecards",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "Software Scorecard Dashboard API is running!"}


# Project endpoints
@app.post("/projects", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate, 
    db: Session = Depends(database.get_db)
):
    """Create a new project"""
    # Check if project with same name already exists
    db_project = crud.get_project_by_name(db, name=project.name)
    if db_project:
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    
    return crud.create_project(db=db, project=project)


@app.get("/projects", response_model=List[schemas.Project])
def list_projects(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db)
):
    """Get all projects"""
    return crud.get_projects(db, skip=skip, limit=limit)


# Scorecard endpoints
@app.post("/scorecards", response_model=schemas.Scorecard)
def create_scorecard(
    scorecard: schemas.ScorecardCreate,
    db: Session = Depends(database.get_db)
):
    """Submit a new scorecard with feedback"""
    # Verify project exists
    project = crud.get_project_by_id(db, project_id=scorecard.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validate scores are between 0 and 100
    scores = [
        scorecard.automation_score,
        scorecard.performance_score,
        scorecard.security_score,
        scorecard.cicd_score
    ]
    
    for score in scores:
        if not (0 <= score <= 100):
            raise HTTPException(status_code=400, detail="Scores must be between 0 and 100")
    
    return crud.create_scorecard_with_feedback(db=db, scorecard=scorecard)


@app.get("/scorecards", response_model=List[schemas.ScorecardWithProject])
def list_scorecards(
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """Get scorecards, optionally filtered by project"""
    scorecards = crud.get_scorecards_by_project(
        db, project_id=project_id, skip=skip, limit=limit
    )
    
    # Convert to response format with project name
    result = []
    for scorecard in scorecards:
        scorecard_data = schemas.ScorecardWithProject(
            id=scorecard.id,
            project_id=scorecard.project_id,
            project_name=scorecard.project.name,
            date=scorecard.date,
            automation_score=scorecard.automation_score,
            performance_score=scorecard.performance_score,
            security_score=scorecard.security_score,
            cicd_score=scorecard.cicd_score,
            created_at=scorecard.created_at,
            feedback=scorecard.feedback
        )
        result.append(scorecard_data)
    
    return result


@app.get("/scorecards/{scorecard_id}/pdf")
def get_scorecard_pdf(
    scorecard_id: int,
    db: Session = Depends(database.get_db)
):
    """Generate and return PDF report for a scorecard"""
    scorecard = crud.get_scorecard_by_id(db, scorecard_id=scorecard_id)
    if not scorecard:
        raise HTTPException(status_code=404, detail="Scorecard not found")
    
    # Generate PDF
    pdf_bytes = generate_pdf_report(scorecard)
    
    # Return PDF as response
    filename = f"scorecard_{scorecard.project.name}_{scorecard.date}.pdf"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/pdf"
    }
    
    return Response(content=pdf_bytes, headers=headers, media_type="application/pdf")


@app.get("/scorecards/{scorecard_id}", response_model=schemas.Scorecard)
def get_scorecard(
    scorecard_id: int,
    db: Session = Depends(database.get_db)
):
    """Get a specific scorecard with all details"""
    scorecard = crud.get_scorecard_by_id(db, scorecard_id=scorecard_id)
    if not scorecard:
        raise HTTPException(status_code=404, detail="Scorecard not found")
    
    return scorecard


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
