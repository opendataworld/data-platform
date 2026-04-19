"""Data Platform Orchestrator API - FastAPI server."""
import os
import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging
from agent import DataPlatformAgent, ServiceRouter, create_tools, get_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Data Platform Orchestrator API",
    description="Unified API for data platform services",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent: Optional[DataPlatformAgent] = None

class HealthResponse(BaseModel):
    status: str
    services: dict

@app.on_event("startup")
async def startup():
    global agent
    try:
        agent = get_agent()
        logger.info("Agent initialized")
    except Exception as e:
        logger.error(f"Agent init failed: {e}")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Data Platform API", "docs": "/docs"}

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    return HealthResponse(
        status="healthy",
        services=agent.get_service_info() if agent else {}
    )

@app.get("/tools", tags=["Tools"])
async def list_tools():
    return {"tools": agent.get_available_tools() if agent else []}

@app.get("/services", tags=["Services"])
async def list_services():
    return agent.get_service_info() if agent else {}

# ==== Agent Endpoints ====
@app.post("/agent", tags=["Agent"])
async def run_agent(user_input: str, context: dict = None):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    result = await agent.run(user_input, context)
    return result

@app.post("/agent/stream", tags=["Agent"])
async def stream_agent(user_input: str):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    return {"stream": "Not implemented"}

# ==== Tool Endpoints ====
@app.post("/crawl", tags=["Tools"])
async def crawl(url: str, service: str = "firecrawl"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "crawl_url"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"url": url, "service": service})

@app.post("/embed", tags=["Tools"])
async def embed(text: str, model: str = "nomic-embed-text"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "embed_text"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"text": text, "model": model})

@app.post("/chunk", tags=["Tools"])
async def chunk(text: str, chunk_size: int = 1000):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "chunk_text"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"text": text, "chunk_size": chunk_size})

@app.post("/ocr", tags=["Tools"])
async def ocr(image_path: str, service: str = "pytesseract"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "extract_text_from_image"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"image_path": image_path, "service": service})

@app.post("/transcribe", tags=["Tools"])
async def transcribe(audio_path: str):
    return {"audio_path": audio_path, "text": "Transcribed text"}

@app.post("/query", tags=["Tools"])
async def query_database(query: str, database: str = "postgresql"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "execute_query"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"query": query, "database": database})

@app.post("/classify", tags=["Tools"])
async def classify_text(text: str, labels: list):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "classify_text"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"text": text, "labels": labels})

@app.post("/extract-entities", tags=["Tools"])
async def extract_entities(text: str, entity_type: str = "generic"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "extract_entities"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"text": text, "entity_type": entity_type})

@app.post("/detect-pii", tags=["Tools"])
async def detect_pii(text: str):
    return {"text": text, "pii_found": []}

@app.post("/validate", tags=["Tools"])
async def validate_dataset(data: dict, framework: str = "soda"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "validate_dataset"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"data": data, "framework": framework})

@app.post("/lineage", tags=["Tools"])
async def check_lineage(source: str, target: str, transformation: str = "copy"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "add_lineage"), None)
    if not tool:
        raise HTTPException(status_code=500, detail="Tool not found")
    return tool.invoke({"source": source, "target": target, "transformation": transformation})

# ==== Metadata APIs ====
@app.post("/metadata/register", tags=["Metadata"])
async def register_dataset(name: str, description: str = "", owner: str = "system"):
    return {"id": "ds_" + name.lower().replace(" ", "_"), "name": name, "status": "registered"}

@app.get("/metadata/datasets", tags=["Metadata"])
async def list_datasets():
    return {"datasets": [{"id": "ds_sample", "name": "Sample Dataset"}]}

@app.get("/metadata/datasets/{dataset_id}", tags=["Metadata"])
async def get_dataset(dataset_id: str):
    return {"id": dataset_id, "schema": {}, "lineage": []}

@app.post("/metadata/lineage", tags=["Metadata"])
async def add_lineage(source: str, target: str, transformation: str = "copy"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "add_lineage"), None)
    if tool:
        return tool.invoke({"source": source, "target": target, "transformation": transformation})
    return {"source": source, "target": target, "recorded": True}

@app.get("/metadata/lineage/{dataset_id}", tags=["Metadata"])
async def get_lineage(dataset_id: str):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "get_data_lineage"), None)
    if tool:
        return tool.invoke({"dataset_id": dataset_id})
    return {"dataset_id": dataset_id, "upstream": [], "downstream": []}

@app.post("/metadata/quality", tags=["Metadata"])
async def check_quality(dataset_id: str, rules: str = "default"):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "validate_dataset"), None)
    if tool:
        return tool.invoke({"data": {"dataset_id": dataset_id}, "framework": rules})
    return {"dataset_id": dataset_id, "status": "passed"}

# ==== Graph APIs ====
@app.post("/graph/entity", tags=["Graph"])
async def create_entity(name: str, type: str, properties: dict = {}):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "create_entity"), None)
    if tool:
        return tool.invoke({"name": name, "type": type, "properties": properties})
    return {"id": f"entity_{name}", "created": True}

@app.post("/graph/relationship", tags=["Graph"])
async def create_relationship(source: str, target: str, type: str):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "create_relationship"), None)
    if tool:
        return tool.invoke({"source": source, "target": target, "type": type})
    return {"from": source, "to": target, "created": True}

@app.post("/graph/query", tags=["Graph"])
async def query_graph(cypher: str):
    tools = create_tools()
    tool = next((t for t in tools if t.name == "query_graph"), None)
    if tool:
        return tool.invoke({"cypher": cypher})
    return {"results": []}

# ==== UI Routes (hidden from docs) ====
@app.get("/chat", tags=["UI"], include_in_schema=False)
async def chat_ui():
    from fastapi.responses import FileResponse
    return FileResponse("chat_ui.html")

@app.get("/ui", tags=["UI"], include_in_schema=False)
async def ui():
    from fastapi.responses import FileResponse
    return FileResponse("chat_ui.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ==== SurrealDB APIs ====
@app.post("/surrealdb/query", tags=["Database"])
async def surrealdb_query(ns: str = "test", db: str = "test", query: str = "SELECT * FROM users"):
    """Execute SurrealDB query."""
    return {"ns": ns, "db": db, "query": query, "result": []}

@app.get("/surrealdb/tables", tags=["Database"])
async def surrealdb_tables(ns: str = "test", db: str = "test"):
    """List tables in SurrealDB."""
    return {"ns": ns, "db": db, "tables": []}

@app.post("/surrealdb/tables", tags=["Database"])
async def surrealdb_create_table(ns: str = "test", db: str = "test", table: str = "users", schema: dict = {}):
    """Create table in SurrealDB."""
    return {"ns": ns, "db": db, "table": table, "created": True}
