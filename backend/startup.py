import asyncio
from backend.Agent.orchestrator.coordinator import Coordinator
from backend.Agent.orchestrator.registry import AgentRegistry
from backend.agents.job_hunt_agent import JobHuntAgent
from backend.agents.resume_agent import ResumeAgent
from backend.agents.interview_agent import InterviewAgent
from backend.agents.outreach_agent import OutreachAgent
from backend.agents.profile_agent import ProfileAgent
from backend.database.engine import init_db
from backend.llm.ollama_client import OllamaClient

async def startup():
    # Initialize database
    init_db()
    
    # Initialize LLM client
    ollama = OllamaClient()
    if not ollama.check_connection():
        print("⚠ Ollama not running. Start with: ollama serve")
    
    # Create agent registry
    registry = AgentRegistry()
    registry.register("job_hunt", JobHuntAgent(ollama))
    registry.register("resume", ResumeAgent(ollama))
    registry.register("interview", InterviewAgent(ollama))
    registry.register("outreach", OutreachAgent(ollama))
    registry.register("profile", ProfileAgent(ollama))
    
    # Create coordinator
    coordinator = Coordinator(registry)
    
    return coordinator

if __name__ == "__main__":
    asyncio.run(startup())
    print("Career OS initialized")