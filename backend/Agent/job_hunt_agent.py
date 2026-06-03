from backend.Agent.base_agent import BaseAgent

class JobHuntAgent(BaseAgent):
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def execute(self, payload: dict) -> dict:
        keywords = payload.get("keywords", [])
        locations = payload.get("locations", [])
        sources = payload.get("sources", ["linkedin", "indeed"])
        
        # TODO: Implement job scraping from multiple sources
        # Return normalized job list
        return {"jobs": [], "status": "initialized"}