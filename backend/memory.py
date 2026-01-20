import uuid
from typing import List, Dict, Any
from threading import Lock
from datetime import datetime, timedelta


class SessionMemory:
    """In-memory session storage with thread-safe operations"""
    
    def __init__(self, session_timeout_hours: int = 24):
        self._sessions: Dict[str, List[Dict[str, Any]]] = {}
        self._session_timestamps: Dict[str, datetime] = {}
        self._lock = Lock()
        self.session_timeout = timedelta(hours=session_timeout_hours)
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())
    
    def validate_session(self, session_id: str) -> bool:
        """Check if session exists and is valid"""
        with self._lock:
            if session_id not in self._sessions:
                return False
            
            # Check if session has expired
            if session_id in self._session_timestamps:
                if datetime.utcnow() - self._session_timestamps[session_id] > self.session_timeout:
                    # Clean up expired session
                    del self._sessions[session_id]
                    del self._session_timestamps[session_id]
                    return False
            
            return True
    
    def create_session(self, session_id: str) -> None:
        """Create a new session"""
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
                self._session_timestamps[session_id] = datetime.utcnow()
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to session history"""
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
            
            self._sessions[session_id].append({
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Update session timestamp
            self._session_timestamps[session_id] = datetime.utcnow()
    
    def get_history(self, session_id: str, max_messages: int = 10) -> List[Dict[str, Any]]:
        """Retrieve conversation history for a session"""
        with self._lock:
            if session_id not in self._sessions:
                return []
            
            # Return last N messages
            return self._sessions[session_id][-max_messages:]
    
    def get_context(self, session_id: str, max_messages: int = 5) -> str:
        """Get formatted context from recent conversation history"""
        history = self.get_history(session_id, max_messages)
        
        if not history:
            return ""
        
        context_parts = []
        for msg in history:
            role = msg["role"].upper()
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n\n".join(context_parts)
    
    def clear_session(self, session_id: str) -> None:
        """Clear all messages from a session"""
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id] = []
                self._session_timestamps[session_id] = datetime.utcnow()
    
    def delete_session(self, session_id: str) -> None:
        """Delete a session completely"""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
            if session_id in self._session_timestamps:
                del self._session_timestamps[session_id]
    
    def cleanup_expired_sessions(self) -> int:
        """Remove all expired sessions, returns count of removed sessions"""
        with self._lock:
            expired = []
            current_time = datetime.utcnow()
            
            for session_id, timestamp in self._session_timestamps.items():
                if current_time - timestamp > self.session_timeout:
                    expired.append(session_id)
            
            for session_id in expired:
                del self._sessions[session_id]
                del self._session_timestamps[session_id]
            
            return len(expired)


# Global session memory instance
session_memory = SessionMemory()
