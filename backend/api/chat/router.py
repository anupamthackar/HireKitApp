from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    actions: Optional[list] = []

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    message = request.message.lower()

    if "job" in message or "hunt" in message:
        return ChatResponse(
            response="I'll help you hunt for iOS jobs. Should I run the job hunt agent now?",
            actions=["job_hunt"]
        )
    elif "resume" in message:
        return ChatResponse(
            response="I can generate a tailored resume for your target job.",
            actions=["resume"]
        )
    elif "interview" in message:
        return ChatResponse(
            response="Let's prepare for your interview. What type of questions would you like?",
            actions=["interview"]
        )
    else:
        return ChatResponse(response="How can I help with your career today?")