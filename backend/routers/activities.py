import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Activity, Project
from schemas import ActivityCreate, ActivityResponse, CSVUploadResponse
from routers.auth import get_current_user

router = APIRouter(prefix="/activity", tags=["Activities"])


def calculate_metrics(activity: Activity) -> Activity:
    """Calculate code churn and instability score"""
    activity.code_churn = activity.lines_added + activity.lines_deleted
    
    # Simple instability score based on files modified and commits
    if activity.commit_count > 0:
        activity.instability_score = (
            (activity.files_modified / activity.commit_count) * 
            (activity.bug_count + 1)
        )
    else:
        activity.instability_score = 0
    
    return activity


@router.post("/manual", response_model=ActivityResponse, status_code=201)
def create_activity_manual(
    activity: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project exists and user has access
    project = db.query(Project).filter(
        Project.id == activity.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    new_activity = Activity(
        project_id=activity.project_id,
        user_id=current_user.id,
        developer_name=activity.developer_name,
        commit_count=activity.commit_count,
        lines_added=activity.lines_added,
        lines_deleted=activity.lines_deleted,
        files_modified=activity.files_modified,
        module_name=activity.module_name,
        bug_count=activity.bug_count
    )
    
    new_activity = calculate_metrics(new_activity)
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


@router.post("/upload", response_model=CSVUploadResponse)
async def upload_csv(
    project_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project exists
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Read CSV
    contents = await file.read()
    import io
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    # Validate required columns
    required_columns = ['developer_name', 'module_name']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing)}"
        )
    
    # Fill missing optional columns with defaults
    optional_columns = ['commit_count', 'lines_added', 'lines_deleted', 'files_modified', 'bug_count']
    for col in optional_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Create activities
    activities = []
    for _, row in df.iterrows():
        activity = Activity(
            project_id=project_id,
            user_id=current_user.id,
            developer_name=row['developer_name'],
            commit_count=int(row.get('commit_count', 0)),
            lines_added=int(row.get('lines_added', 0)),
            lines_deleted=int(row.get('lines_deleted', 0)),
            files_modified=int(row.get('files_modified', 0)),
            module_name=row['module_name'],
            bug_count=int(row.get('bug_count', 0))
        )
        activity = calculate_metrics(activity)
        db.add(activity)
        activities.append(activity)
    
    db.commit()
    
    # Refresh to get IDs
    for activity in activities:
        db.refresh(activity)
    
    return CSVUploadResponse(
        message=f"Successfully uploaded {len(activities)} activities",
        records_added=len(activities),
        activities=activities
    )


@router.get("", response_model=List[ActivityResponse])
def get_activities(
    project_id: int = None,
    developer_name: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Activity).join(Project).filter(Project.owner_id == current_user.id)
    
    if project_id:
        query = query.filter(Activity.project_id == project_id)
    if developer_name:
        query = query.filter(Activity.developer_name == developer_name)
    
    return query.all()


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    activity = db.query(Activity).join(Project).filter(
        Activity.id == activity_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return activity
