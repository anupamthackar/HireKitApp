from backend.Agent.base_agent import BaseAgent

class ProfileAgent(BaseAgent):
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def execute(self, payload: dict) -> dict:
        profile = payload.get("profile")
        
        # TODO: Manage user profile and skills
        return {"profile": profile}