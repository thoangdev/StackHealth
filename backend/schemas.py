from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Feedback schemas
class FeedbackBase(BaseModel):
    area: str
    comment: Optional[str] = None
    tool_recommendation: Optional[str] = None
    marked_for_improvement: bool = False


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int
    scorecard_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Scorecard schemas
class ScorecardBase(BaseModel):
    project_id: int
    date: date
    automation_score: float
    performance_score: float
    security_score: float
    cicd_score: float


class ScorecardCreate(ScorecardBase):
    feedback: Optional[List[FeedbackCreate]] = []


class Scorecard(ScorecardBase):
    id: int
    created_at: datetime
    project: Project
    feedback: List[Feedback] = []

    class Config:
        from_attributes = True


# Response schemas
class ScorecardWithProject(BaseModel):
    id: int
    project_id: int
    project_name: str
    date: date
    automation_score: float
    performance_score: float
    security_score: float
    cicd_score: float
    created_at: datetime
    feedback: List[Feedback] = []

    class Config:
        from_attributes = True
