import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

class MemoryManager:
    """Manages agent memory and session state"""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(__file__).parent.parent.parent.parent / "data"
        self.session_file = self.data_dir / "session.json"

    def save_session(self, session_id: str, data: Dict[str, Any]):
        """Save session state to disk"""
        sessions = self._load_sessions()
        sessions[session_id] = {
            **data,
            "updated_at": datetime.now().isoformat()
        }
        self.session_file.write_text(json.dumps(sessions, indent=2))

    def load_session(self, session_id: str) -> Dict[str, Any]:
        """Load session state from disk"""
        sessions = self._load_sessions()
        return sessions.get(session_id, {})

    def _load_sessions(self) -> Dict:
        if not self.session_file.exists():
            return {}
        try:
            return json.loads(self.session_file.read_text())
        except:
            return {}

    def add_chat_message(self, session_id: str, role: str, content: str):
        """Add message to session chat history"""
        session = self.load_session(session_id)
        messages = session.get("messages", [])
        messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        session["messages"] = messages
        self.save_session(session_id, session)