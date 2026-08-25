import enum
import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    OA = "OA"
    PHONE_SCREEN = "PHONE_SCREEN"
    ONSITE = "ONSITE"
    OFFER = "OFFER"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")

class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, index=True, nullable=False)
    website = Column(String, nullable=True)

    applications = relationship("Application", back_populates="company")

class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, index=True)
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    job_url = Column(String, nullable=True)
    last_status_update = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="applications")
    company = relationship("Company", back_populates="applications")
    rounds = relationship("InterviewRound", back_populates="application", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="application", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="application", cascade="all, delete-orphan")

class InterviewRound(Base):
    __tablename__ = "interview_rounds"

    id = Column(String, primary_key=True, default=generate_uuid)
    application_id = Column(String, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    round_name = Column(String, nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)

    application = relationship("Application", back_populates="rounds")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String, primary_key=True, default=generate_uuid)
    application_id = Column(String, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)

    application = relationship("Application", back_populates="contacts")

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, default=generate_uuid)
    application_id = Column(String, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="notes")