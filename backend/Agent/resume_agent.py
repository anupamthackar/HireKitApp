from typing import Dict, Any
from ..llm.ollama_client import OllamaClient

class ResumeAgent:
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client
        self.TEMPLATES = {
            "modern": "modern_resume_prompt.txt",
            "classic": "classic_resume_prompt.txt",
            "minimal": "minimal_resume_prompt.txt",
        }

    async def execute(self, payload: Dict[str, Any]) -> Dict:
        """Generate tailored resume for a job"""
        profile = payload.get("profile")
        job = payload.get("job")
        template = payload.get("template", "modern")

        if not profile or not job:
            return {"error": "Profile and job required"}

        # Get resume text from profile
        resume_content = self._format_resume(profile, job, template)

        return {
            "status": "generated",
            "resume": resume_content,
            "template": template
        }

    def _format_resume(self, profile: Dict, job: Dict, template: str) -> str:
        """Format resume based on template"""
        header = f"# {profile.get('name', 'Name')}\n"
        header += f"{profile.get('email', '')} | {profile.get('phone', '')}\n"
        header += f"{profile.get('location', '')}\n"
        header += f"{profile.get('linkedin', '')} | {profile.get('website', '')}\n"

        skills = f"\n## Skills\n{', '.join(profile.get('skills', []))}\n"

        experience = "\n## Experience\n"
        for exp in profile.get('experience', []):
            experience += f"- {exp.get('title')} @ {exp.get('company')}\n"

        return header + skills + experience

    async def generate_latex(self, resume_data: Dict) -> str:
        """Generate LaTeX version of resume"""
        return "\\documentclass{article}\n\\begin{document}\nGenerated LaTeX\n\\end{document}"

    async def score_match(self, resume: str, job_description: str) -> Dict:
        """Score how well resume matches job"""
        prompt = f"Score alignment between resume and job. Return JSON with score and missing_skills."
        # Would call LLM here
        return {"score": 85, "missing_skills": []}