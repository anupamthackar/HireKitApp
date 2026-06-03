from typing import Dict, Any, Callable, List
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowStep:
    def __init__(self, name: str, action: Callable, next_step: str = None):
        self.name = name
        self.action = action
        self.next_step = next_step
        self.status = TaskStatus.PENDING

class WorkflowEngine:
    def __init__(self):
        self.steps: Dict[str, WorkflowStep] = {}
        self.current_step: str = None

    def add_step(self, step: WorkflowStep):
        self.steps[step.name] = step

    async def run(self, initial_step: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.current_step = initial_step
        results = {}

        while self.current_step:
            step = self.steps.get(self.current_step)
            if not step:
                break

            step.status = TaskStatus.RUNNING
            try:
                result = await step.action(payload) if callable(step.action) else step.action(payload)
                results[step.name] = result
                step.status = TaskStatus.COMPLETED
                self.current_step = step.next_step
            except Exception as e:
                step.status = TaskStatus.FAILED
                results[step.name] = {"error": str(e)}
                break

        return {
            "status": "completed",
            "results": results,
            "steps": {name: s.status.value for name, s in self.steps.items()}
        }