from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .models import ApplicationStatus

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Application Schemas
class ApplicationCreate(BaseModel):
    company_name: str
    role: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_url: Optional[str] = None
    status: Optional[ApplicationStatus] = ApplicationStatus.APPLIED

class ApplicationResponse(BaseModel):
    id: str
    role: str
    status: ApplicationStatus
    applied_date: datetime
    salary_min: Optional[int]
    salary_max: Optional[int]
    job_url: Optional[str]

    class Config:
        from_attributes = True