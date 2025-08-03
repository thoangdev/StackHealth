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


# Security Scorecard specific fields (25 points total)
class SecurityScorecard(BaseModel):
    # Static & Dynamic Testing (9 points)
    sast: bool  # 2 pts
    dast: bool  # 2 pts
    sast_dast_in_ci: bool  # 3 pts
    triaging_findings: bool  # 2 pts
    
    # Tooling & Integration (7 points)
    secrets_scanning: bool  # 1 pt
    sca_tool_used: bool  # 2 pts
    cve_alerts: bool  # 2 pts
    security_tools: bool  # 2 pts
    
    # Policies & Practices (9 points)
    threat_modeling: bool  # 2 pts
    compliance: bool  # 1 pt
    training: bool  # 1 pt
    bug_bounty_policy: bool  # 1 pt
    owasp_samm_integration: bool  # 4 pts


# Automation Scorecard fields (44 points total)
class AutomationScorecard(BaseModel):
    # Test Automation Framework (28 points)
    automated_testing: bool  # 1 pt
    dedicated_environment: bool  # 2 pts
    testing_framework: bool  # 2 pts
    external_updates: bool  # 1 pt
    quick_setup: bool  # 0.5 pts
    source_controlled: bool  # 2 pts
    seeded_data: bool  # 1 pt
    test_independence: bool  # -3 pts if false
    data_reseeding: bool  # 2 pts
    test_subsets: bool  # 2 pts
    rapid_updates: bool  # 1 pt
    database_automation: bool  # 1 pt
    post_deploy_sanity: bool  # 2 pts
    sanity_independence: bool  # -1 pt if false
    smoke_testing: bool  # 2 pts
    test_reporting: bool  # 2 pts
    notification_integration: bool  # 0.5 pts
    
    # Test Coverage Assessment (16 points)
    api_coverage: str  # "0%", "1-20%", "20-40%", "40-60%", "60-80%", "80-100%"
    functional_coverage: str  # "0%", "1-20%", "20-40%", "40-100%"


# Performance Scorecard fields (25 points total)
class PerformanceScorecard(BaseModel):
    # Performance Strategy & Tooling (9 points)
    regular_testing: bool  # 2 pts
    dedicated_tools: bool  # 1 pt
    ci_integration: bool  # 3 pts
    defined_thresholds: bool  # 1 pt
    trend_tracking: bool  # 2 pts
    
    # Test Coverage & Types (7 points)
    test_types: str  # "smoke", "load", "stress", "spike", "soak" (1-5 pts)
    production_like_env: bool  # 2 pts
    workflow_coverage: str  # "0%", "1-20%", "20-50%", "50-100%"
    
    # Metrics & Observability (9 points)
    latency_throughput: bool  # 1 pt
    error_saturation: bool  # 1 pt
    dashboard_viz: bool  # 2 pts
    automated_alerting: bool  # 2 pts
    monitoring_integration: bool  # 3 pts


# CI/CD Scorecard fields (42 points total)
class CICDScorecard(BaseModel):
    # DORA Metrics (16 points)
    deployment_frequency: str  # "on-demand", "daily", "weekly", "monthly"
    lead_time: str  # "<1hour", "<1day", "<1week", ">1week"
    recovery_time: str  # "<1hour", "<1day", "<1week", ">1week"
    change_failure_rate: str  # "0-15%", "16-30%", "31-45%", ">45%"
    
    # Pipeline Maturity (26 points)
    automated_builds: bool  # 4 pts
    automated_tests: bool  # 4 pts
    automated_deployment: bool  # 4 pts
    rollback_capability: bool  # 4 pts
    blue_green_deployment: bool  # 3 pts
    canary_releases: bool  # 3 pts
    infrastructure_as_code: bool  # 4 pts


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
