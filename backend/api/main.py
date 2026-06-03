from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat.router import router as chat_router
from backend.api.jobs.router import router as jobs_router

app = FastAPI(title="HireKit API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(jobs_router)

@app.get("/")
async def root():
    return {"message": "HireKit Career OS API", "status": "running"}