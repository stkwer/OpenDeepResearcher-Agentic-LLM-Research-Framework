import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List
import logging

from models import (
    ResearchRequest, ResearchResponse, ErrorResponse,
    Conversation, ConversationCreate, ConversationUpdate, Message
)
from memory import session_memory
from database import db
from graph.research_graph import build_graph

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Deep Research API",
    description="AI-powered research assistant with session memory",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build research graph
try:
    research_graph = build_graph()
    logger.info("Research graph initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize research graph: {e}")
    research_graph = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Deep Research API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "graph_initialized": research_graph is not None
    }


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """
    Main research endpoint
    
    Accepts a research query and session ID, processes it through the
    LangGraph pipeline, and returns a comprehensive research report.
    """
    try:
        # Validate research graph is initialized
        if research_graph is None:
            raise HTTPException(
                status_code=503,
                detail="Research graph not initialized. Check API keys and configuration."
            )
        
        # Get or create conversation from database
        conversation = db.get_conversation_by_session(request.session_id)
        conversation_id = None
        
        if conversation:
            conversation_id = conversation["id"]
        
        # Validate or create session (for backward compatibility)
        if not session_memory.validate_session(request.session_id):
            session_memory.create_session(request.session_id)
            logger.info(f"Created new session: {request.session_id}")
        
        # Get conversation context from database if available
        context = ""
        if conversation_id:
            messages = db.get_messages(conversation_id, limit=6)  # Get last 3 exchanges
            if messages:
                context_parts = []
                for msg in messages[-6:]:  # Last 6 messages (3 user + 3 assistant)
                    role = msg["role"].upper()
                    content = msg["content"]
                    context_parts.append(f"{role}: {content}")
                context = "\n\n".join(context_parts)
        
        # Prepare topic with context if available
        topic = request.message
        if context:
            # Inject context for multi-turn conversations
            topic = f"Previous context:\n{context}\n\nNew query: {request.message}"
            logger.info(f"Using context for session {request.session_id}")
        
        # Store user message in memory (for backward compatibility)
        session_memory.add_message(request.session_id, "user", request.message)
        
        # Store user message in database if conversation exists
        if conversation_id:
            db.add_message(conversation_id, "user", request.message)
        
        # Run research pipeline
        logger.info(f"Processing research query: {request.message[:50]}...")
        result = research_graph.invoke({"topic": topic})
        
        # Extract research report
        research_report = result.get("summary", "No summary generated")
        
        # Store assistant response in memory (for backward compatibility)
        session_memory.add_message(request.session_id, "assistant", research_report)
        
        # Store assistant response in database if conversation exists
        if conversation_id:
            db.add_message(conversation_id, "assistant", research_report)
        
        logger.info(f"Research completed for session {request.session_id}")
        
        return ResearchResponse(
            response=research_report,
            session_id=request.session_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing research request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/session/clear")
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    try:
        session_memory.clear_session(session_id)
        logger.info(f"Cleared session: {session_id}")
        return {"message": "Session cleared successfully", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/new")
async def new_session():
    """Generate a new session ID"""
    session_id = session_memory.generate_session_id()
    session_memory.create_session(session_id)
    logger.info(f"Generated new session: {session_id}")
    return {"session_id": session_id}


# ============================================
# Conversation Management Endpoints
# ============================================

@app.get("/conversations", response_model=List[Conversation])
async def get_conversations():
    """Get all conversations"""
    try:
        conversations = db.get_all_conversations()
        return conversations
    except Exception as e:
        logger.error(f"Error fetching conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all messages"""
    try:
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/conversations", response_model=Conversation)
async def create_conversation(conversation: ConversationCreate):
    """Create a new conversation"""
    try:
        new_conversation = db.create_conversation(
            conversation.id,
            conversation.session_id,
            conversation.title
        )
        logger.info(f"Created conversation: {conversation.id}")
        return new_conversation
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(conversation_id: str, update: ConversationUpdate):
    """Update a conversation"""
    try:
        if update.title:
            db.update_conversation_title(conversation_id, update.title)
        
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        db.delete_conversation(conversation_id)
        logger.info(f"Deleted conversation: {conversation_id}")
        return {"message": "Conversation deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting Deep Research API...")
    logger.info(f"CORS enabled for: http://localhost:5173")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down Deep Research API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

