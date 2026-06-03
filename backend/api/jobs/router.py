from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from backend.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])
job_service = JobService()

class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    location: str
    salary: Optional[str]
    score: int
    match: str
    sponsorship: bool = False
    sp_status: Optional[str]
    source: Optional[str]
    url: Optional[str]

@router.get("/", response_model=List[JobResponse])
async def list_jobs(limit: int = 50, match: Optional[str] = None, sponsored: bool = False):
    return job_service.list_jobs(limit, match, sponsored)

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    raise HTTPException(status_code=404, detail="Job not found")