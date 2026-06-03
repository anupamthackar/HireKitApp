from typing import Dict, Any, List
from ..llm.ollama_client import OllamaClient

class InterviewAgent:
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client
        self.TECH_STACK = ["Swift", "SwiftUI", "iOS", "CoreML", "SPM", "Combine", "UIKit"]

    async def execute(self, payload: Dict[str, Any]) -> Dict:
        """Generate interview questions based on job and profile"""
        resume = payload.get("resume")
        job = payload.get("job")
        question_type = payload.get("type", "technical")

        questions = []
        if question_type == "technical":
            questions = await self._generate_technical_questions(resume, job)
        elif question_type == "behavioral":
            questions = await self._generate_behavioral_questions(resume, job)
        elif question_type == "system_design":
            questions = await self._generate_system_design_questions(job)

        return {
            "status": "generated",
            "questions": questions,
            "type": question_type
        }

    async def _generate_technical_questions(self, resume: Dict, job: Dict) -> List[Dict]:
        """Generate technical iOS/Swift questions"""
        base_questions = [
            {
                "question": "Explain Swift's memory management. How does ARC work?",
                "category": "Swift",
                "difficulty": "medium"
            },
            {
                "question": "What are the key differences between SwiftUI and UIKit?",
                "category": "iOS",
                "difficulty": "easy"
            },
            {
                "question": "How would you integrate CoreML into an iOS app?",
                "category": "CoreML",
                "difficulty": "hard"
            }
        ]
        
        # Filter by tech stack mentioned in job
        tech_stack = job.get("description", "").lower()
        filtered = []
        for q in base_questions:
            if any(tech.lower() in tech_stack for tech in q["category"]):
                filtered.append(q)

        return filtered or base_questions

    async def _generate_behavioral_questions(self, resume: Dict, job: Dict) -> List[Dict]:
        """Generate behavioral questions using STAR format"""
        return [
            {
                "question": "Tell me about a challenging iOS project you worked on",
                "category": "experience",
                "format": "STAR"
            },
            {
                "question": "Describe a time you had to optimize app performance",
                "category": "problem_solving",
                "format": "STAR"
            }
        ]

    async def _generate_system_design_questions(self, job: Dict) -> List[Dict]:
        """Generate system design questions"""
        return [
            {
                "question": "Design a scalable networking layer for an iOS app",
                "category": "architecture",
                "difficulty": "hard"
            }
        ]

    async def evaluate_answer(self, question: str, answer: str) -> Dict:
        """Evaluate interview answer with LLM"""
        # Would call LLM to evaluate
        return {"score": 80, "feedback": "Good answer with room for improvement"}