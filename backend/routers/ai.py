from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import User, Project, Activity
from schemas import RiskPrediction, AIInsight
from ml.risk_model import predict_risk as ml_predict_risk
from routers.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/predict-risk", response_model=RiskPrediction)
def predict_module_risk(
    module_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict risk level for a specific module"""
    # Get activities for this module
    activities = db.query(Activity).join(Project).filter(
        Project.owner_id == current_user.id,
        Activity.module_name == module_name
    ).all()
    
    if not activities:
        # Use default values if no data
        result = ml_predict_risk(
            commit_count=1,
            lines_added=10,
            lines_deleted=5,
            files_modified=1,
            bug_count=0,
            modification_frequency=1.0
        )
    else:
        # Aggregate data from activities
        total_commits = sum(a.commit_count for a in activities)
        total_lines_added = sum(a.lines_added for a in activities)
        total_lines_deleted = sum(a.lines_deleted for a in activities)
        total_files_modified = sum(a.files_modified for a in activities)
        total_bugs = sum(a.bug_count for a in activities)
        
        # Modification frequency based on number of activities
        modification_freq = len(activities)
        
        result = ml_predict_risk(
            commit_count=total_commits,
            lines_added=total_lines_added,
            lines_deleted=total_lines_deleted,
            files_modified=total_files_modified,
            bug_count=total_bugs,
            modification_frequency=modification_freq
        )
    
    return RiskPrediction(
        module_name=module_name,
        risk_score=result['risk_score'],
        risk_level=result['risk_level'],
        factors=result['factors'],
        recommendation=result['recommendation']
    )


@router.get("/risk-analysis", response_model=List[RiskPrediction])
def get_risk_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk analysis for all modules"""
    activities = db.query(Activity).join(Project).filter(
        Project.owner_id == current_user.id
    ).all()
    
    # Group by module
    module_data = {}
    for activity in activities:
        if activity.module_name not in module_data:
            module_data[activity.module_name] = {
                'commit_count': 0,
                'lines_added': 0,
                'lines_deleted': 0,
                'files_modified': 0,
                'bug_count': 0,
                'activity_count': 0
            }
        module_data[activity.module_name]['commit_count'] += activity.commit_count
        module_data[activity.module_name]['lines_added'] += activity.lines_added
        module_data[activity.module_name]['lines_deleted'] += activity.lines_deleted
        module_data[activity.module_name]['files_modified'] += activity.files_modified
        module_data[activity.module_name]['bug_count'] += activity.bug_count
        module_data[activity.module_name]['activity_count'] += 1
    
    # Get predictions for each module
    predictions = []
    for module_name, data in module_data.items():
        result = ml_predict_risk(
            commit_count=data['commit_count'],
            lines_added=data['lines_added'],
            lines_deleted=data['lines_deleted'],
            files_modified=data['files_modified'],
            bug_count=data['bug_count'],
            modification_frequency=data['activity_count']
        )
        
        predictions.append(RiskPrediction(
            module_name=module_name,
            risk_score=result['risk_score'],
            risk_level=result['risk_level'],
            factors=result['factors'],
            recommendation=result['recommendation']
        ))
    
    return sorted(predictions, key=lambda x: x.risk_score, reverse=True)


@router.get("/insights", response_model=List[AIInsight])
def get_ai_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated insights and recommendations"""
    insights = []
    
    # Get activities
    activities = db.query(Activity).join(Project).filter(
        Project.owner_id == current_user.id
    ).all()
    
    if not activities:
        return [
            AIInsight(
                id=1,
                insight_type="info",
                message="No activity data available. Upload development activity data to get AI insights.",
                created_at=datetime.utcnow()
            )
        ]
    
    # Group by module for analysis
    module_data = {}
    for activity in activities:
        if activity.module_name not in module_data:
            module_data[activity.module_name] = {
                'commits': 0,
                'bugs': 0,
                'churn': 0,
                'files': 0
            }
        module_data[activity.module_name]['commits'] += activity.commit_count
        module_data[activity.module_name]['bugs'] += activity.bug_count
        module_data[activity.module_name]['churn'] += activity.code_churn
        module_data[activity.module_name]['files'] += activity.files_modified
    
    insight_id = 1
    
    # Generate insights based on data
    for module_name, data in module_data.items():
        # High churn insight
        if data['churn'] > 500:
            insights.append(AIInsight(
                id=insight_id,
                insight_type="warning",
                message=f"Module '{module_name}' has high code churn ({data['churn']} lines). Consider refactoring.",
                module_name=module_name,
                created_at=datetime.utcnow()
            ))
            insight_id += 1
        
        # High bug count insight
        if data['bugs'] > 10:
            insights.append(AIInsight(
                id=insight_id,
                insight_type="danger",
                message=f"Module '{module_name}' has {data['bugs']} bugs reported. Prioritize bug fixes.",
                module_name=module_name,
                created_at=datetime.utcnow()
            ))
            insight_id += 1
        
        # High commit frequency insight
        if data['commits'] > 50:
            insights.append(AIInsight(
                id=insight_id,
                insight_type="info",
                message=f"Module '{module_name}' is frequently modified ({data['commits']} commits). Ensure proper testing.",
                module_name=module_name,
                created_at=datetime.utcnow()
            ))
            insight_id += 1
    
    # Add general insights
    total_bugs = sum(d['bugs'] for d in module_data.values())
    if total_bugs > 20:
        insights.append(AIInsight(
            id=insight_id,
            insight_type="warning",
            message="Overall bug count is high across all modules. Consider implementing more rigorous testing.",
            created_at=datetime.utcnow()
        ))
        insight_id += 1
    
    # Developer insights
    dev_commits = {}
    for activity in activities:
        if activity.developer_name not in dev_commits:
            dev_commits[activity.developer_name] = 0
        dev_commits[activity.developer_name] += activity.commit_count
    
    max_commits_dev = max(dev_commits.items(), key=lambda x: x[1])
    if max_commits_dev[1] > 0:
        insights.append(AIInsight(
            id=insight_id,
            insight_type="info",
            message=f"Developer '{max_commits_dev[0]}' has the highest commit count ({max_commits_dev[1]}). Consider peer reviews.",
            created_at=datetime.utcnow()
        ))
    
    if not insights:
        insights.append(AIInsight(
            id=1,
            insight_type="success",
            message="Your codebase looks healthy! No major issues detected.",
            created_at=datetime.utcnow()
        ))
    
    return insights
