from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Application, Company
from ..schemas import ApplicationCreate, ApplicationResponse
from ..auth import get_current_user

router = APIRouter(tags=["Applications"])

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    app_data: ApplicationCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Find or create company
    company = db.query(Company).filter(Company.name == app_data.company_name).first()
    if not company:
        company = Company(name=app_data.company_name)
        db.add(company)
        db.commit()
        db.refresh(company)

    new_app = Application(
        user_id=current_user.id,
        company_id=company.id,
        role=app_data.role,
        salary_min=app_data.salary_min,
        salary_max=app_data.salary_max,
        job_url=app_data.job_url,
        status=app_data.status
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@router.get("/", response_model=List[ApplicationResponse])
def get_user_applications(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(Application).filter(Application.user_id == current_user.id).all()

@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    app_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    app_item = db.query(Application).filter(
        Application.id == app_id, 
        Application.user_id == current_user.id
    ).first()
    
    if not app_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        
    db.delete(app_item)
    db.commit()
    return None