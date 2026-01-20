from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ResearchRequest(BaseModel):
    """Request model for research endpoint"""
    message: str = Field(..., min_length=1, description="User's research query")
    session_id: str = Field(..., description="Unique session identifier")


class ResearchResponse(BaseModel):
    """Response model for research endpoint"""
    response: str = Field(..., description="AI-generated research report")
    session_id: str = Field(..., description="Session identifier")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


class Message(BaseModel):
    """Message model"""
    role: str
    content: str
    timestamp: str


class Conversation(BaseModel):
    """Conversation model"""
    id: str
    session_id: str
    title: str
    created_at: str
    updated_at: str
    messages: List[Message] = []


class ConversationCreate(BaseModel):
    """Request model for creating a conversation"""
    id: str
    session_id: str
    title: str = "New Research"


class ConversationUpdate(BaseModel):
    """Request model for updating a conversation"""
    title: Optional[str] = None

