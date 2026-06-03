from typing import Dict, Any
import asyncio

class TaskRouter:
    def __init__(self, coordinator):
        self.coordinator = coordinator
    
    async def route(self, task_name: str, payload: dict) -> dict:
        return await self.coordinator.run(task_name, payload)