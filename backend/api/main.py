from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="HireKit API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    source: str
    url: str
    salary: Optional[str]
    score: int
    match: str
    sponsorship: bool = False
    sp_status: Optional[str]

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict]

class ChatResponse(BaseModel):
    response: str
    actions: Optional[List[str]]

@app.get("/")
async def root():
    return {"message": "HireKit Career OS API"}

@app.get("/jobs", response_model=List[Job])
async def get_jobs(limit: int = 50, match: Optional[str] = None, sponsored: bool = False):
    # TODO: Query database
    return []

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # TODO: Route to appropriate agent
    return ChatResponse(
        response="I'm processing your request...",
        actions=["job_hunt", "resume", "interview"]
    )

@app.post("/agents/job-hunt")
async def run_job_hunt(payload: dict):
    # TODO: Execute JobHuntAgent
    return {"status": "started", "jobs_found": 0}