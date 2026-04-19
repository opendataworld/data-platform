"""
Chat Interface for Data Platform Agent
Exposes agent as a chat API
"""
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio

app = FastAPI(title="Data Platform Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==== Chat Models ====

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    context: Optional[Dict] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    tools_used: Optional[List[str]] = None
    services_deployed: Optional[List[str]] = None


# ==== Sessions Store ====

sessions: Dict[str, List[Message]] = {}


# ==== Chat Endpoints ====

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the agent - uses skills automatically
    """
    session_id = request.session_id
    
    # Initialize session if needed
    if session_id not in sessions:
        sessions[session_id] = []
    
    # Add user message
    sessions[session_id].append(Message(role="user", content=request.message))
    
    try:
        # Import and run agent
        from agent import DataPlatformAgent
        
        agent = DataPlatformAgent()
        result = await agent.run(request.message)
        
        response_text = result.get("response", str(result))
        tools_used = result.get("tools_used", [])
        services_deployed = result.get("deployed_services", [])
        
        # Add assistant message
        sessions[session_id].append(Message(role="assistant", content=response_text))
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            tools_used=tools_used,
            services_deployed=services_deployed
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/sessions/{session_id}/history")
async def get_history(session_id: str) -> List[Message]:
    """Get chat history for a session"""
    return sessions.get(session_id, [])


@app.delete("/chat/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session"""
    if session_id in sessions:
        del sessions[session_id]
    return {"status": "deleted", "session_id": session_id}


@app.get("/chat/sessions")
async def list_sessions() -> List[str]:
    """List all chat sessions"""
    return list(sessions.keys())


# ==== Health ====

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "chat"}


# ==== If running directly ====

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)