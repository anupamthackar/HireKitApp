import pytest
from backend.Agent.job_hunt_agent import JobHuntAgent
from backend.Agent.resume_agent import ResumeAgent
from backend.Agent.interview_agent import InterviewAgent
from backend.llm.ollama_client import OllamaClient

def test_job_hunt_agent_priority():
    ollama = OllamaClient()
    agent = JobHuntAgent(ollama)
    assert agent.get_priority("Dubai, UAE") == 1
    assert agent.get_priority("Bangalore, India") == 3
    assert agent.get_priority("Berlin, Germany") == 4
    assert agent.get_priority("Remote") == 5

def test_job_hunt_agent_dedupe():
    ollama = OllamaClient()
    agent = JobHuntAgent(ollama)
    jobs = [
        {"company": "A", "title": "iOS Dev", "location": "UAE"},
        {"company": "A", "title": "iOS Dev", "location": "UAE"},
        {"company": "B", "title": "iOS Dev", "location": "UAE"},
    ]
    unique = agent._deduplicate(jobs)
    assert len(unique) == 2

def test_resume_agent_format():
    ollama = OllamaClient()
    agent = ResumeAgent(ollama)
    profile = {"name": "Test", "email": "test@test.com", "skills": ["Swift", "iOS"]}
    job = {"title": "iOS Engineer", "company": "TestCorp", "location": "UAE"}
    result = agent._format_resume(profile, job, "modern")
    assert "Test" in result
    assert "Swift" in result

def test_interview_agent_questions():
    ollama = OllamaClient()
    agent = InterviewAgent(ollama)
    
    import asyncio
    tech = asyncio.run(agent._generate_technical_questions({}, {}))
    assert len(tech) > 0
    assert tech[0]["question"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])