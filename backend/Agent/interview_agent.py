from backend.Agent.base_agent import BaseAgent

class InterviewAgent(BaseAgent):
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def execute(self, payload: dict) -> dict:
        resume = payload.get("resume")
        job = payload.get("job")
        
        # TODO: Generate interview questions and STAR answers
        return {"questions": [], "answers": []}