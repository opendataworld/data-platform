"""
FastAPI server for the LangGraph Orchestrator Agent
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os

from agent import DataPlatformAgent, ServiceRouter, create_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Data Platform Orchestrator API",
    description="LangGraph agent orchestrating data platform services",
    version="0.1.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request models
class AgentRequest(BaseModel):
    input: str = Field(..., description="User input to the agent")
    context: Optional[dict] = Field(default_factory=dict, description="Additional context")
    model: Optional[str] = Field(default="llama3", description="LLM model to use")


class HealthResponse(BaseModel):
    status: str
    services: dict


class ToolInfo(BaseModel):
    name: str
    description: str


class ServiceInfo(BaseModel):
    category: str
    services: list[str]


# Initialize agent
agent: Optional[DataPlatformAgent] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup."""
    global agent
    try:
        agent = DataPlatformAgent(
            model=os.getenv("LLM_MODEL", "llama3"),
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434")
        )
        logger.info("Agent initialized successfully")
    except Exception as e:
        logger.warning(f"Agent not initialized: {e}")
        agent = None


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "name": "Data Platform Orchestrator API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy" if agent else "starting",
        "services": {
            "ingest": ServiceRouter.INGEST_SERVICES,
            "embedding": ServiceRouter.EMBEDDING_SERVICES,
            "ocr": ServiceRouter.OCR_SERVICES,
            "image": ServiceRouter.IMAGE_SERVICES,
            "llm": ServiceRouter.LLM_SERVICES,
            "chunking": ServiceRouter.CHUNKING_SERVICES,
            "governance": ServiceRouter.GOVERNANCE_SERVICES
        }
    }


@app.get("/tools", tags=["Tools"])
async def list_tools():
    """List available tools."""
    tools = create_tools()
    return [
        {"name": t.name, "description": t.description}
        for t in tools
    ]


@app.get("/services", tags=["Services"])
async def list_services():
    """List available services by category."""
    from agent import ServiceRegistry
    return {
        "data_platforms": ServiceRegistry.DATA_WAREHOUSE + ServiceRegistry.DATA_LAKE,
        "data_architecture": ServiceRegistry.DATA_CATALOGS,
        "data_engineering": ServiceRegistry.ORCHESTRATION + ServiceRegistry.STREAMING,
        "data_transfer": ServiceRegistry.TRANSFER,
        "data_integration": ServiceRegistry.ETL,
        "data_quality": ServiceRegistry.QUALITY,
        "data_governance": ServiceRegistry.GOVERNANCE,
        "data_democratization": ServiceRegistry.DEMOCRATIZATION,
        "data_optimization": ServiceRegistry.OPTIMIZATION,
        # ML/AI
        "crawl": ServiceRegistry.CRAWL,
        "embedding": ServiceRegistry.EMBEDDING,
        "ocr": ServiceRegistry.OCR,
        "image": ServiceRegistry.IMAGE,
        "llm": ServiceRegistry.LLM,
        "nlp": ServiceRegistry.NLP,
        "entity_resolution": ServiceRegistry.ENTITY_RESOLUTION,
        "chunking": ServiceRegistry.CHUNKING,
        "vector": ServiceRegistry.VECTOR,
        "clustering": ServiceRegistry.CLUSTERING,
        "workflow": ServiceRegistry.WORKFLOW,
    }


@app.post("/agent", tags=["Agent"])
async def run_agent(request: AgentRequest):
    """Run the orchestrator agent."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        result = await agent.run(request.input, request.context)
        return result
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/stream", tags=["Agent"])
async def run_agent_stream(request: AgentRequest):
    """Run the agent with streaming response."""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    # For now, return a simple response
    # Full streaming would require async generation
    try:
        result = await agent.run(request.input, request.context)
        return {
            "input": request.input,
            "response": result.get("messages", []),
            "tools_used": result.get("tools_used", [])
        }
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- Tool-specific endpoints ---

@app.post("/crawl", tags=["Tools"])
async def crawl_url(url: str, service: str = "jina-reader"):
    """Crawl a URL and extract content."""
    from langchain_core.tools import tool
    
    tools = create_tools()
    crawl_tool = next((t for t in tools if t.name == "crawl_and_extract"), None)
    
    if not crawl_tool:
        raise HTTPException(status_code=500, detail="Crawl tool not found")
    
    result = crawl_tool.invoke({"url": url, "service": service})
    return {"result": result}


@app.post("/embed", tags=["Tools"])
async def embed_text(text: str, service: str = "sentence-transformers"):
    """Create embeddings for text."""
    tools = create_tools()
    embed_tool = next((t for t in tools if t.name == "embed_text"), None)
    
    if not embed_tool:
        raise HTTPException(status_code=500, detail="Embed tool not found")
    
    result = embed_tool.invoke({"text": text, "service": service})
    return {"result": result}


@app.post("/chunk", tags=["Tools"])
async def chunk_text(text: str, method: str = "recursive", chunk_size: int = 1000):
    """Chunk text into smaller pieces."""
    tools = create_tools()
    chunk_tool = next((t for t in tools if t.name == "chunk_text"), None)
    
    if not chunk_tool:
        raise HTTPException(status_code=500, detail="Chunk tool not found")
    
    result = chunk_tool.invoke({
        "text": text,
        "method": method,
        "chunk_size": chunk_size
    })
    return {"result": result}


@app.post("/ocr", tags=["Tools"])
async def run_ocr(image_path: str, service: str = "tesseract"):
    """Run OCR on an image."""
    tools = create_tools()
    ocr_tool = next((t for t in tools if t.name == "run_ocr"), None)
    
    if not ocr_tool:
        raise HTTPException(status_code=500, detail="OCR tool not found")
    
    result = ocr_tool.invoke({"image_path": image_path, "service": service})
    return {"result": result}


@app.post("/transcribe", tags=["Tools"])
async def transcribe_audio(audio_path: str, service: str = "whisper"):
    """Transcribe audio to text."""
    tools = create_tools()
    transcribe_tool = next((t for t in tools if t.name == "transcribe_audio"), None)
    
    if not transcribe_tool:
        raise HTTPException(status_code=500, detail="Transcribe tool not found")
    
    result = transcribe_tool.invoke({"audio_path": audio_path, "service": service})
    return {"result": result}


@app.post("/query", tags=["Tools"])
async def query_llm(prompt: str, model: str = "llama3"):
    """Query the LLM."""
    tools = create_tools()
    llm_tool = next((t for t in tools if t.name == "query_llm"), None)
    
    if not llm_tool:
        raise HTTPException(status_code=500, detail="LLM tool not found")
    
    result = llm_tool.invoke({"prompt": prompt, "model": model})
    return {"result": result}


@app.post("/classify", tags=["Tools"])
async def classify_taxonomy(text: str, taxonomy: str = "iptc-media-topics"):
    """Classify text into taxonomy."""
    tools = create_tools()
    classify_tool = next((t for t in tools if t.name == "classify_taxonomy"), None)
    
    if not classify_tool:
        raise HTTPException(status_code=500, detail="Classify tool not found")
    
    result = classify_tool.invoke({"text": text, "taxonomy": taxonomy})
    return {"result": result}


@app.post("/extract-entities", tags=["Tools"])
async def extract_entities(text: str, service: str = "spacy-ner"):
    """Extract named entities."""
    tools = create_tools()
    ner_tool = next((t for t in tools if t.name == "extract_entities"), None)
    
    if not ner_tool:
        raise HTTPException(status_code=500, detail="NER tool not found")
    
    result = ner_tool.invoke({"text": text, "service": service})
    return {"result": result}


@app.post("/detect-pii", tags=["Tools"])
async def detect_pii(text: str, service: str = "presidio-analyzer"):
    """Detect PII in text."""
    tools = create_tools()
    pii_tool = next((t for t in tools if t.name == "detect_pii"), None)
    
    if not pii_tool:
        raise HTTPException(status_code=500, detail="PII tool not found")
    
    result = pii_tool.invoke({"text": text, "service": service})
    return {"result": result}


@app.post("/validate", tags=["Tools"])
async def validate_data(source: str, framework: str = "great-expectations"):
    """Validate data quality."""
    tools = create_tools()
    validate_tool = next((t for t in tools if t.name == "validate_data"), None)
    
    if not validate_tool:
        raise HTTPException(status_code=500, detail="Validate tool not found")
    
    result = validate_tool.invoke({"source": source, "framework": framework})
    return {"result": result}


@app.post("/lineage", tags=["Tools"])
async def check_lineage(asset: str, framework: str = "marquez"):
    """Check data lineage."""
    tools = create_tools()
    lineage_tool = next((t for t in tools if t.name == "check_lineage"), None)
    
    if not lineage_tool:
        raise HTTPException(status_code=500, detail="Lineage tool not found")
    
    result = lineage_tool.invoke({"asset": asset, "framework": framework})
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)