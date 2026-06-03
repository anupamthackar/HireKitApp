import os
import asyncio
import sys

sys.path.insert(0, '.')

from backend.Agent.orchestrator.coordinator import Coordinator
from backend.Agent.orchestrator.registry import AgentRegistry
from backend.Agent.job_hunt_agent import JobHuntAgent
from backend.Agent.resume_agent import ResumeAgent
from backend.Agent.interview_agent import InterviewAgent
from backend.Agent.outreach_agent import OutreachAgent
from backend.Agent.profile_agent import ProfileAgent
from backend.database.engine import init_db
from backend.llm.ollama_client import OllamaClient

async def main():
    print("🚀 Initializing HireKit Career OS...")

    # Initialize database
    init_db()
    print("✓ Database initialized")

    # Initialize LLM client
    ollama = OllamaClient()
    if ollama.check_connection():
        print("✓ Ollama connected")
    else:
        print("⚠ Ollama not running. Start with: ollama serve")

    # Create agent registry
    registry = AgentRegistry()
    registry.register("job_hunt", JobHuntAgent(ollama))
    registry.register("resume", ResumeAgent(ollama))
    registry.register("interview", InterviewAgent(ollama))
    registry.register("outreach", OutreachAgent(ollama))
    registry.register("profile", ProfileAgent(ollama))

    print("✓ Agents registered:", registry.list_agents())

    # Create coordinator
    coordinator = Coordinator(registry)

    print("\n✅ Career OS ready!")
    return coordinator

if __name__ == "__main__":
    asyncio.run(main())