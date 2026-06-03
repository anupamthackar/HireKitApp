from backend.Agent.base_agent import BaseAgent

class ResumeAgent(BaseAgent):
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def execute(self, payload: dict) -> dict:
        profile = payload.get("profile")
        job = payload.get("job")
        
        # TODO: Generate tailored resume
        return {"resume": None, "status": "generated"}