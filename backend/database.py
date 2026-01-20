import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import threading


class ConversationDatabase:
    """SQLite database for persistent conversation storage"""
    
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_database()
    
    def _get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def _init_database(self):
        """Initialize database schema"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                session_id TEXT UNIQUE NOT NULL,
                title TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        
        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation 
            ON messages(conversation_id)
        """)
        
        conn.commit()
    
    def create_conversation(self, conversation_id: str, session_id: str, title: str = "New Research") -> Dict[str, Any]:
        """Create a new conversation"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO conversations (id, session_id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (conversation_id, session_id, title, now, now))
        
        conn.commit()
        
        return {
            "id": conversation_id,
            "session_id": session_id,
            "title": title,
            "created_at": now,
            "updated_at": now,
            "messages": []
        }
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get a conversation with all its messages"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get conversation
        cursor.execute("""
            SELECT * FROM conversations WHERE id = ?
        """, (conversation_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        conversation = dict(row)
        
        # Get messages
        cursor.execute("""
            SELECT role, content, timestamp 
            FROM messages 
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        """, (conversation_id,))
        
        messages = [dict(msg) for msg in cursor.fetchall()]
        conversation["messages"] = messages
        
        return conversation
    
    def get_all_conversations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all conversations ordered by most recent"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*, 
                   COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            GROUP BY c.id
            ORDER BY c.updated_at DESC
            LIMIT ?
        """, (limit,))
        
        conversations = []
        for row in cursor.fetchall():
            conv = dict(row)
            # Get messages for this conversation
            cursor.execute("""
                SELECT role, content, timestamp 
                FROM messages 
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
            """, (conv["id"],))
            conv["messages"] = [dict(msg) for msg in cursor.fetchall()]
            conversations.append(conv)
        
        return conversations
    
    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """Add a message to a conversation"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.utcnow().isoformat()
        
        # Insert message
        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (conversation_id, role, content, now))
        
        # Update conversation timestamp
        cursor.execute("""
            UPDATE conversations 
            SET updated_at = ?
            WHERE id = ?
        """, (now, conversation_id))
        
        conn.commit()
    
    def update_conversation_title(self, conversation_id: str, title: str) -> None:
        """Update conversation title"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE conversations 
            SET title = ?, updated_at = ?
            WHERE id = ?
        """, (title, datetime.utcnow().isoformat(), conversation_id))
        
        conn.commit()
    
    def delete_conversation(self, conversation_id: str) -> None:
        """Delete a conversation and all its messages"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        conn.commit()
    
    def get_conversation_by_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation by session ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id FROM conversations WHERE session_id = ?
        """, (session_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return self.get_conversation(row["id"])
    
    def get_messages(self, conversation_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get messages for a conversation"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT role, content, timestamp 
            FROM messages 
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
            LIMIT ?
        """, (conversation_id, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def clear_conversation_messages(self, conversation_id: str) -> None:
        """Clear all messages from a conversation"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
        conn.commit()


# Global database instance
db = ConversationDatabase()
