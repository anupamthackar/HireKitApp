from backend.Agent.base_agent import BaseAgent

class OutreachAgent(BaseAgent):
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def execute(self, payload: dict) -> dict:
        job = payload.get("job")
        recruiter = payload.get("recruiter")
        
        # TODO: Generate outreach messages
        return {"messages": []}