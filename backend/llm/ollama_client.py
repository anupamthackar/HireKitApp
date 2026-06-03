import requests
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")

class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_URL):
        self.base_url = base_url
    
    async def chat(self, model: str, system_prompt: str, message: str) -> str:
        payload = {
            "model": model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        }
        try:
            r = requests.post(self.base_url, json=payload, timeout=60)
            return r.json()["message"]["content"].strip()
        except Exception as e:
            return f'Error: {e}'
    
    def check_connection(self) -> bool:
        try:
            requests.get(self.base_url.replace("/api/chat", ""), timeout=3)
            return True
        except:
            return False