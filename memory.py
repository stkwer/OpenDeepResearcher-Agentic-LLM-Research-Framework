import json
import os
from datetime import datetime


class SessionMemory:
    def __init__(self, session_dir="sessions"):
        self.session_dir = session_dir
        os.makedirs(self.session_dir, exist_ok=True)

    def save(self, topic: str, data: dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic.replace(" ", "_").lower()
        filename = f"{safe_topic}_{timestamp}.json"
        path = os.path.join(self.session_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return path

    # ✅ NEW: list saved sessions
    def list_sessions(self):
        return sorted(
            os.listdir(self.session_dir),
            reverse=True
        )

    # ✅ NEW: load a session
    def load(self, filename: str):
        path = os.path.join(self.session_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
