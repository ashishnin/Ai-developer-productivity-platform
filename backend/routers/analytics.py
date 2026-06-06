from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import User, Project, Activity
from schemas import ProductivityMetrics, ChurnMetrics, DashboardSummary
from routers.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Total projects
    total_projects = db.query(Project).filter(Project.owner_id == current_user.id).count()
    
    # Total developers (unique developer names in activities)
    total_developers = db.query(Activity.developer_name).join(Project).filter(
        Project.owner_id == current_user.id
    ).distinct().count()
    
    # Get all activities for calculations
    activities = db.query(Activity).join(Project).filter(
        Project.owner_id == current_user.id
    ).all()
    
    # Calculate average productivity
    if activities:
        total_commits = sum(a.commit_count for a in activities)
        total_lines_added = sum(a.lines_added for a in activities)
        total_lines_deleted = sum(a.lines_deleted for a in activities)
        
        # Simple productivity score based on commits and code contribution
        avg_productivity = min(100, (total_commits * 2 + total_lines_added / 100) / 10)
    else:
        total_commits = 0
        total_lines_added = 0
        total_lines_deleted = 0
        avg_productivity = 0
    
    # High risk modules (instability score > 5)
    high_risk_modules = sum(1 for a in activities if a.instability_score > 5)
    
    # Total code churn
    total_code_churn = sum(a.code_churn for a in activities)
    
    return DashboardSummary(
        total_projects=total_projects,
        total_developers=total_developers,
        avg_productivity=round(avg_productivity, 2),
        high_risk_modules=high_risk_modules,
        total_commits=total_commits,
        total_code_churn=total_code_churn
    )


@router.get("/productivity", response_model=List[ProductivityMetrics])
def get_productivity_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activities = db.query(Activity).join(Project).filter(
        Project.owner_id == current_user.id
    ).all()
    
    # Group by developer
    dev_stats = {}
    for activity in activities:
        if activity.developer_name not in dev_stats:
            dev_stats[activity.developer_name] = {
                'total_commits': 0,
                'total_lines_added': 0,
                'total_lines_deleted': 0,
                'total_files_modified': 0,
                'total_bugs': 0
            }
        dev_stats[activity.developer_name]['total_commits'] += activity.commit_count
        dev_stats[activity.developer_name]['total_lines_added'] += activity.lines_added
        dev_stats[activity.developer_name]['total_lines_deleted'] += activity.lines_deleted
        dev_stats[activity.developer_name]['total_files_modified'] += activity.files_modified
        dev_stats[activity.developer_name]['total_bugs'] += activity.bug_count
    
    # Calculate total for percentages
    total_commits = sum(s['total_commits'] for s in dev_stats.values())
    
    # Calculate metrics for each developer
    metrics = []
    for dev_name, stats in dev_stats.items():
        # Productivity score calculation
        productivity_score = min(100, (
            stats['total_commits'] * 3 +
            stats['total_lines_added'] / 50 +
            stats['total_files_modified'] * 2 -
            stats['total_bugs'] * 5
        ) / 10)
        
        # Contribution percentage
        contribution_pct = (stats['total_commits'] / total_commits * 100) if total_commits > 0 else 0
        
        metrics.append(ProductivityMetrics(
            developer_name=dev_name,
            total_commits=stats['total_commits'],
            total_lines_added=stats['total_lines_added'],
            total_lines_deleted=stats['total_lines_deleted'],
            total_files_modified=stats['total_files_modified'],
            total_bugs=stats['total_bugs'],
            productivity_score=round(productivity_score, 2),
            contribution_percentage=round(contribution_pct, 2)
        ))
    
    return sorted(metrics, key=lambda x: x.productivity_score, reverse=True)


@router.get("/churn", response_model=List[ChurnMetrics])
def get_churn_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activities = db.query(Activity).join(Project).filter(
        Project.owner_id == current_user.id
    ).all()
    
    # Group by module
    module_stats = {}
    for activity in activities:
        if activity.module_name not in module_stats:
            module_stats[activity.module_name] = {
                'code_churn': 0,
                'commit_count': 0,
                'files_modified': 0
            }
        module_stats[activity.module_name]['code_churn'] += activity.code_churn
        module_stats[activity.module_name]['commit_count'] += activity.commit_count
        module_stats[activity.module_name]['files_modified'] += activity.files_modified
    
    # Calculate metrics
    metrics = []
    for module_name, stats in module_stats.items():
        commit_frequency = stats['commit_count']
        instability = (stats['files_modified'] / max(1, stats['commit_count'])) * 10
        
        metrics.append(ChurnMetrics(
            module_name=module_name,
            code_churn=stats['code_churn'],
            commit_frequency=commit_frequency,
            instability_score=round(instability, 2)
        ))
    
    return sorted(metrics, key=lambda x: x.instability_score, reverse=True)


@router.get("/commits")
def get_commit_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activities = db.query(Activity).join(Project).filter(
        Project.owner_id == current_user.id
    ).all()
    
    # Group by developer and module
    commit_data = {}
    for activity in activities:
        key = f"{activity.developer_name} - {activity.module_name}"
        if key not in commit_data:
            commit_data[key] = {
                'developer': activity.developer_name,
                'module': activity.module_name,
                'commits': 0,
                'lines_added': 0,
                'lines_deleted': 0,
                'bugs': 0
            }
        commit_data[key]['commits'] += activity.commit_count
        commit_data[key]['lines_added'] += activity.lines_added
        commit_data[key]['lines_deleted'] += activity.lines_deleted
        commit_data[key]['bugs'] += activity.bug_count
    
    return list(commit_data.values())
