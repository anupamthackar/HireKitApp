from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    headline: Optional[str] = None
    experience_years: int = 0
    metadata_json: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(index=True)
    title: str
    company: str
    location: str
    source: str
    url: str
    salary: Optional[str] = None
    description: Optional[str] = None
    score: int = 0
    match: str = "L"
    sponsorship: int = 0
    sp_status: Optional[str] = None
    found_at: datetime = Field(default_factory=datetime.utcnow)

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id")
    status: str = "draft"
    applied_at: Optional[datetime] = None
    follow_up_at: Optional[datetime] = None

class Outreach(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id")
    message_type: str  # linkedin, email
    content: str
    status: str = "draft"  # draft, sent, replied, interview, rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)