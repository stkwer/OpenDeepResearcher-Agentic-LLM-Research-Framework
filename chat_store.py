import json
import uuid
from pathlib import Path

CHAT_DIR = Path("chats")
CHAT_DIR.mkdir(exist_ok=True)

def new_chat():
    chat_id = str(uuid.uuid4())
    return {
        "id": chat_id,
        "title": "New Research",
        "messages": []
    }

def save_chat(chat):
    path = CHAT_DIR / f"{chat['id']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=2)

def load_chats():
    chats = []
    for file in CHAT_DIR.glob("*.json"):
        with open(file, encoding="utf-8") as f:
            chats.append(json.load(f))
    return sorted(chats, key=lambda x: x["title"])

def delete_chat(chat_id):
    path = CHAT_DIR / f"{chat_id}.json"
    if path.exists():
        path.unlink()