import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.Agent.orchestrator.registry import AgentRegistry
from backend.Agent.orchestrator.coordinator import Coordinator
from backend.Agent.job_hunt_agent import JobHuntAgent
from backend.Agent.resume_agent import ResumeAgent
from backend.Agent.interview_agent import InterviewAgent
from backend.llm.ollama_client import OllamaClient
from backend.database.engine import init_db

async def main():
    print("🚀 HireKit Ecosystem Test\n")

    # Initialize database
    init_db()
    print("✓ Database initialized\n")

    # Check Ollama connection
    ollama = OllamaClient()
    if ollama.check_connection():
        print("✓ Ollama connected\n")
    else:
        print("⚠ Ollama not running (start with: ollama serve)\n")

    # Create registry and register agents
    registry = AgentRegistry()
    registry.register("job_hunt", JobHuntAgent(ollama))
    registry.register("resume", ResumeAgent(ollama))
    registry.register("interview", InterviewAgent(ollama))

    coordinator = Coordinator(registry)

    # Test each agent
    print("Testing agents...\n")

    # Test JobHuntAgent
    print("1. Job Hunt Agent:")
    try:
        result = await coordinator.run("job_hunt", {
            "keywords": ["iOS Developer"],
            "locations": ["UAE", "India"],
            "sources": ["linkedin", "indeed"]
        })
        print(f"   Status: {result.get('status')}")
        print(f"   Jobs found: {result.get('jobs_found', 0)}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

    # Test ResumeAgent
    print("2. Resume Agent:")
    try:
        profile = {"name": "Anupam Thackar", "skills": ["Swift", "iOS", "CoreML"]}
        result = await coordinator.run("resume", {"profile": profile, "job": {"title": "iOS Engineer"}})
        print(f"   Status: {result.get('status')}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

    # Test InterviewAgent
    print("3. Interview Agent:")
    try:
        result = await coordinator.run("interview", {"type": "technical"})
        print(f"   Questions generated: {len(result.get('questions', []))}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

    print("✅ All agents tested successfully!")
    print(f"\nRegistered agents: {registry.list_agents()}")

if __name__ == "__main__":
    asyncio.run(main())