from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Auth Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "developer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# Project Schemas
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    repo_link: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    repo_link: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    repo_link: Optional[str]
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Activity Schemas
class ActivityCreate(BaseModel):
    project_id: int
    developer_name: str
    commit_count: int = 0
    lines_added: int = 0
    lines_deleted: int = 0
    files_modified: int = 0
    module_name: str
    bug_count: int = 0


class ActivityResponse(BaseModel):
    id: int
    project_id: int
    developer_name: str
    commit_count: int
    lines_added: int
    lines_deleted: int
    files_modified: int
    module_name: str
    bug_count: int
    code_churn: float
    instability_score: float
    last_modified_date: datetime

    class Config:
        from_attributes = True


# Analytics Schemas
class ProductivityMetrics(BaseModel):
    developer_name: str
    total_commits: int
    total_lines_added: int
    total_lines_deleted: int
    total_files_modified: int
    total_bugs: int
    productivity_score: float
    contribution_percentage: float


class ChurnMetrics(BaseModel):
    module_name: str
    code_churn: float
    commit_frequency: float
    instability_score: float


class DashboardSummary(BaseModel):
    total_projects: int
    total_developers: int
    avg_productivity: float
    high_risk_modules: int
    total_commits: int
    total_code_churn: float


# AI Schemas
class RiskPrediction(BaseModel):
    module_name: str
    risk_score: float
    risk_level: str
    factors: List[str]
    recommendation: str


class AIInsight(BaseModel):
    id: int
    insight_type: str
    message: str
    module_name: Optional[str] = None
    created_at: datetime


# CSV Upload Schema
class CSVUploadResponse(BaseModel):
    message: str
    records_added: int
    activities: List[ActivityResponse]
