from typing import Dict, Any

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, Any] = {}
    
    def register(self, name: str, agent):
        self.agents[name] = agent
    
    def get(self, name: str):
        return self.agents.get(name)
    
    def list_agents(self) -> list:
        return list(self.agents.keys())