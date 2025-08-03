from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any, Union
from datetime import date, datetime


# Authentication schemas
class AdminUserBase(BaseModel):
    email: EmailStr


class AdminUserCreate(AdminUserBase):
    password: str


class AdminUser(AdminUserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Product schemas (renamed from Project)
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Security Scorecard specific fields
class SecurityScorecard(BaseModel):
    sast: bool
    dast: bool
    sast_dast_in_ci: bool
    triaging_findings: bool
    secrets_scanning: bool
    sca_tool_used: bool
    cve_alerts: bool
    pr_enforcement: bool
    training: bool
    threat_modeling: bool
    bug_bounty_policy: bool
    compliance: bool
    secure_design_reviews: bool
    predeployment_threat_modeling: bool


# Automation Scorecard fields
class AutomationScorecard(BaseModel):
    ci_pipeline: bool
    automated_testing: bool
    deployment_automation: bool
    monitoring_alerts: bool
    infrastructure_as_code: bool


# Performance Scorecard fields
class PerformanceScorecard(BaseModel):
    load_testing: bool
    performance_monitoring: bool
    caching_strategy: bool
    database_optimization: bool
    cdn_usage: bool


# CI/CD Scorecard fields
class CICDScorecard(BaseModel):
    automated_builds: bool
    automated_tests: bool
    code_quality_gates: bool
    deployment_pipeline: bool
    rollback_strategy: bool
    environment_parity: bool


# Scorecard schemas
class ScorecardBase(BaseModel):
    product_id: int
    category: str  # "automation", "performance", "security", "cicd"
    date: date


class ScorecardCreate(ScorecardBase):
    breakdown: Union[SecurityScorecard, AutomationScorecard, PerformanceScorecard, CICDScorecard]


class Scorecard(ScorecardBase):
    id: int
    score: float
    breakdown: Dict[str, Any]
    feedback: Optional[str] = None
    tool_suggestions: Optional[str] = None
    created_at: datetime
    product: Product

    class Config:
        from_attributes = True


# Response schemas
class ScorecardWithProduct(BaseModel):
    id: int
    product_id: int
    product_name: str
    category: str
    date: date
    score: float
    breakdown: Dict[str, Any]
    feedback: Optional[str] = None
    tool_suggestions: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TrendData(BaseModel):
    date: date
    score: float
    category: str
