import os
from pathlib import Path
from typing import Dict

PROMPTS_DIR = Path(__file__).parent.parent.parent.parent / "prompts"

class PromptManager:
    def __init__(self):
        self.templates: Dict[str, str] = {}
        self._load_templates()

    def _load_templates(self):
        """Load all prompt templates from disk"""
        for category in ["jobs", "resume", "interview", "outreach"]:
            category_dir = PROMPTS_DIR / category
            if category_dir.exists():
                for file in category_dir.glob("*.txt"):
                    self.templates[f"{category}/{file.stem}"] = file.read_text()

    def get(self, template_name: str) -> str:
        """Get template by name"""
        return self.templates.get(template_name, "")

    def render(self, template_name: str, variables: Dict[str, str]) -> str:
        """Render template with variables"""
        template = self.get(template_name)
        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def list_templates(self) -> list:
        return list(self.templates.keys())