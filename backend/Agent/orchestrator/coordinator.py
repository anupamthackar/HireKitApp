from .registry import AgentRegistry

class Coordinator:
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
    
    async def run(self, task_name: str, payload: dict) -> dict:
        agent = self.registry.get(task_name)
        if not agent:
            raise ValueError(f"No agent registered for '{task_name}'")
        return await agent.execute(payload)