"""
Data Platform Unified API Server
Exposes all data platform services via REST API
"""
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Any
import logging
import os
from datetime import datetime

# Import orchestrator components
from agent import DataPlatformAgent, ServiceRegistry, create_data_management_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Data Platform API",
    description="Unified API for data platform services aligned with IBM Data Management Guide",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models

class CrawlRequest(BaseModel):
    url: str
    service: str = "jina-reader"

class EmbedRequest(BaseModel):
    text: str
    service: str = "sentence-transformers"

class ChunkRequest(BaseModel):
    text: str
    method: str = "recursive"
    chunk_size: int = 1000

class OCRRequest(BaseModel):
    image_path: str
    service: str = "tesseract"

class TranscribeRequest(BaseModel):
    audio_path: str
    service: str = "whisper"

class QueryLLMRequest(BaseModel):
    prompt: str
    model: str = "llama3"

class QualityCheckRequest(BaseModel):
    source: str
    framework: str = "great-expectations"

class ProfilingRequest(BaseModel):
    source: str
    framework: str = "ydata-profiling"

class WorkflowRequest(BaseModel):
    workflow: str
    tool: str = "airflow"

class StreamRequest(BaseModel):
    topic: str
    service: str = "kafka"

class TransferRequest(BaseModel):
    source: str
    destination: str
    service: str = "rclone"

class IntegrationRequest(BaseModel):
    sources: list[str]
    target: str
    service: str = "trino"

class OptimizeRequest(BaseModel):
    source: str
    service: str = "data-optimization"

class LineageRequest(BaseModel):
    asset: str
    service: str = "marquez"

class EntityExtractRequest(BaseModel):
    text: str
    service: str = "spacy-ner"

class PIIRequest(BaseModel):
    text: str
    service: str = "presidio-analyzer"

class TaxonomyRequest(BaseModel):
    text: str
    taxonomy: str = "iptc-media-topics"

# API Routers

crawl_router = APIRouter(prefix="/crawl", tags=["Crawling"])
embed_router = APIRouter(prefix="/embed", tags=["Embedding"])
chunk_router = APIRouter(prefix="/chunk", tags=["Chunking"])
ocr_router = APIRouter(prefix="/ocr", tags=["OCR"])
transcribe_router = APIRouter(prefix="/transcribe", tags=["Speech-to-Text"])
llm_router = APIRouter(prefix="/llm", tags=["LLM"])
quality_router = APIRouter(prefix="/quality", tags=["Data Quality"])
profiling_router = APIRouter(prefix="/profile", tags=["Data Profiling"])
workflow_router = APIRouter(prefix="/workflow", tags=["Data Engineering"])
stream_router = APIRouter(prefix="/stream", tags=["Streaming"])
transfer_router = APIRouter(prefix="/transfer", tags=["Data Transfer"])
integration_router = APIRouter(prefix="/integrate", tags=["Data Integration"])
optimize_router = APIRouter(prefix="/optimize", tags=["Data Optimization"])
lineage_router = APIRouter(prefix="/lineage", tags=["Data Governance"])
ner_router = APIRouter(prefix="/ner", tags=["NLP"])
pii_router = APIRouter(prefix="/pii", tags=["PII Detection"])
taxonomy_router = APIRouter(prefix="/taxonomy", tags=["Classification"])

# ==== Crawling Endpoints ====

@crawl_router.post("/extract")
async def crawl_and_extract(req: CrawlRequest):
    """Crawl a URL and extract content."""
    available = ServiceRegistry.CRAWL
    if req.service not in available:
        req.service = available[0]
    return {
        "url": req.url,
        "service": req.service,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Embedding Endpoints ====

@embed_router.post("/text")
async def embed_text(req: EmbedRequest):
    """Create embeddings for text."""
    available = ServiceRegistry.EMBEDDING
    if req.service not in available:
        req.service = available[0]
    return {
        "service": req.service,
        "text_length": len(req.text),
        "embedding_dim": 384,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Chunking Endpoints ====

@chunk_router.post("/split")
async def chunk_text(req: ChunkRequest):
    """Chunk text into smaller pieces."""
    available = ServiceRegistry.CHUNKING
    if req.method not in available:
        req.method = available[0]
    return {
        "method": req.method,
        "chunk_size": req.chunk_size,
        "text_length": len(req.text),
        "estimated_chunks": len(req.text) // req.chunk_size + 1,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== OCR Endpoints ====

@ocr_router.post("/image")
async def run_ocr(req: OCRRequest):
    """Run OCR on an image."""
    available = ServiceRegistry.OCR
    if req.service not in available:
        req.service = available[0]
    return {
        "service": req.service,
        "image": req.image_path,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Speech-to-Text Endpoints ====

@transcribe_router.post("/audio")
async def transcribe_audio(req: TranscribeRequest):
    """Transcribe audio to text."""
    available = ServiceRegistry.OCR  # Speech services
    if req.service not in available:
        req.service = available[0]
    return {
        "service": req.service,
        "audio": req.audio_path,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== LLM Endpoints ====

@llm_router.post("/query")
async def query_llm(req: QueryLLMRequest):
    """Query the LLM."""
    available = ServiceRegistry.LLM
    if req.model not in available:
        req.model = available[0]
    return {
        "model": req.model,
        "prompt": req.prompt[:100],
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Data Quality Endpoints ====

@quality_router.post("/check")
async def data_quality_check(req: QualityCheckRequest):
    """Check data quality."""
    available = ServiceRegistry.QUALITY
    if req.framework not in available:
        req.framework = available[0]
    return {
        "framework": req.framework,
        "source": req.source,
        "checks": ["accuracy", "completeness", "consistency", "uniqueness", "timeliness"],
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Data Profiling Endpoints ====

@profiling_router.post("/analyze")
async def data_profiling(req: ProfilingRequest):
    """Profile data - generate statistics."""
    available = ["ydata-profiling", "pandas-profiling"]
    if req.framework not in available:
        req.framework = available[0]
    return {
        "framework": req.framework,
        "source": req.source,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Workflow Orchestration Endpoints ====

@workflow_router.post("/run")
async def orchestrate_workflow(req: WorkflowRequest):
    """Orchestrate data workflow."""
    available = ServiceRegistry.ORCHESTRATION
    if req.tool not in available:
        req.tool = available[0]
    return {
        "workflow": req.workflow,
        "tool": req.tool,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Streaming Endpoints ====

@stream_router.post("/publish")
async def stream_data(req: StreamRequest):
    """Publish to data stream."""
    available = ServiceRegistry.STREAMING
    if req.service not in available:
        req.service = available[0]
    return {
        "topic": req.topic,
        "service": req.service,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Data Transfer Endpoints ====

@transfer_router.post("/move")
async def transfer_data(req: TransferRequest):
    """Transfer data between systems."""
    available = ServiceRegistry.TRANSFER
    if req.service not in available:
        req.service = available[0]
    return {
        "source": req.source,
        "destination": req.destination,
        "service": req.service,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Data Integration Endpoints ====

@integration_router.post("/combine")
async def integrate_data(req: IntegrationRequest):
    """Integrate data from multiple sources."""
    available = ServiceRegistry.ETL
    if req.service not in available:
        req.service = available[0]
    return {
        "sources": req.sources,
        "target": req.target,
        "service": req.service,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Data Optimization Endpoints ====

@optimize_router.post("/compress")
async def optimize_data(req: OptimizeRequest):
    """Optimize data."""
    available = ServiceRegistry.OPTIMIZATION
    if req.service not in available:
        req.service = available[0]
    return {
        "source": req.service,
        "service": req.service,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Data Lineage Endpoints ====

@lineage_router.post("/track")
async def check_lineage(req: LineageRequest):
    """Track data lineage."""
    return {
        "asset": req.asset,
        "service": req.service,
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== NER Endpoints ====

@ner_router.post("/extract")
async def extract_entities(req: EntityExtractRequest):
    """Extract named entities."""
    available = ServiceRegistry.NLP
    if req.service not in available:
        req.service = available[0]
    return {
        "text": req.text[:100],
        "service": req.service,
        "entities": [],
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== PII Detection Endpoints ====

@pii_router.post("/detect")
async def detect_pii(req: PIIRequest):
    """Detect PII in text."""
    return {
        "service": req.service,
        "pii_types": [],
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Taxonomy Endpoints ====

@taxonomy_router.post("/classify")
async def classify_taxonomy(req: TaxonomyRequest):
    """Classify text into taxonomy."""
    return {
        "text": req.text[:50],
        "taxonomy": req.taxonomy,
        "categories": [],
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

# ==== Register all routers ====

app.include_router(crawl_router)
app.include_router(embed_router)
app.include_router(chunk_router)
app.include_router(ocr_router)
app.include_router(transcribe_router)
app.include_router(llm_router)
app.include_router(quality_router)
app.include_router(profiling_router)
app.include_router(workflow_router)
app.include_router(stream_router)
app.include_router(transfer_router)
app.include_router(integration_router)
app.include_router(optimize_router)
app.include_router(lineage_router)
app.include_router(ner_router)
app.include_router(pii_router)
app.include_router(taxonomy_router)

# Root endpoint

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Data Platform API",
        "version": "1.0.0",
        "description": "Unified API for data platform services",
        "docs": "/docs",
        "services": "/services"
    }

# Health endpoint

@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "crawl": len(ServiceRegistry.CRAWL),
            "embedding": len(ServiceRegistry.EMBEDDING),
            "llm": len(ServiceRegistry.LLM),
            "quality": len(ServiceRegistry.QUALITY),
            "governance": len(ServiceRegistry.GOVERNANCE),
        }
    }

# Services endpoint

@app.get("/services")
async def list_services():
    """List all available services."""
    return {
        "data_platforms": ServiceRegistry.DATA_WAREHOUSE + ServiceRegistry.DATA_LAKE,
        "data_engineering": ServiceRegistry.ORCHESTRATION + ServiceRegistry.STREAMING,
        "data_transfer": ServiceRegistry.TRANSFER,
        "data_integration": ServiceRegistry.ETL,
        "data_quality": ServiceRegistry.QUALITY,
        "data_governance": ServiceRegistry.GOVERNANCE,
        "crawling": ServiceRegistry.CRAWL,
        "embedding": ServiceRegistry.EMBEDDING,
        "ocr": ServiceRegistry.OCR,
        "llm": ServiceRegistry.LLM,
        "nlp": ServiceRegistry.NLP,
        "entity_resolution": ServiceRegistry.ENTITY_RESOLUTION,
        "chunking": ServiceRegistry.CHUNKING,
        "vector": ServiceRegistry.VECTOR,
        "clustering": ServiceRegistry.CLUSTERING,
        "workflow": ServiceRegistry.WORKFLOW,
        "image": ServiceRegistry.IMAGE,
        "video": ServiceRegistry.VIDEO_GEN,
    }


# ==== AutonomyX Agent Endpoints ====

class AutonomyXAgentRequest(BaseModel):
    agent_name: str
    sponsor_subject_id: str
    tenant_id: str
    allowed_models: list[str]
    allowed_tools: Optional[list[str]] = None
    max_spend_cents: Optional[int] = 50000
    max_requests: Optional[int] = 1000


@app.post("/autonomyx/agents", tags=["AutonomyX"])
async def create_autonomyx_agent(request: AutonomyXAgentRequest):
    """Create an agent following AutonomyX specification."""
    from autonomyx_agent import (
        AutonomyXAgentRegistry, DataPlatformAgentFactory,
        BudgetPolicy, RatePolicy, AgentCreateRequest as AXRequest
    )
    
    registry = AutonomyXAgentRegistry()
    factory = DataPlatformAgentFactory(registry)
    
    ax_request = AXRequest(
        agent_name=request.agent_name,
        agent_type="workflow",
        sponsor_subject_id=request.sponsor_subject_id,
        tenant_id=request.tenant_id,
        allowed_models=request.allowed_models,
        allowed_tools=request.allowed_tools,
        budget_policy=BudgetPolicy(
            measurement_period="month",
            max_spend_cents=request.max_spend_cents
        ),
        rate_policy=RatePolicy(
            window_seconds=3600,
            max_requests=request.max_requests
        )
    )
    
    agent = registry.create_agent(ax_request)
    return {
        "agent_id": agent.agent_id,
        "agent_name": agent.agent_name,
        "status": agent.status,
        "credential": {
            "token": agent.credential.token,
            "expires_at": agent.credential.expires_at.isoformat()
        } if agent.credential else None
    }


@app.get("/autonomyx/agents", tags=["AutonomyX"])
async def list_autonomyx_agents(tenant_id: Optional[str] = None):
    """List all AutonomyX agents."""
    from autonomyx_agent import AutonomyXAgentRegistry
    
    registry = AutonomyXAgentRegistry()
    agents = registry.list_agents(tenant_id=tenant_id)
    
    return {"agents": [{"agent_id": a.agent_id, "agent_name": a.agent_name, "status": a.status, "tenant_id": a.tenant_id} for a in agents]}


@app.post("/autonomyx/agents/{agent_id}/suspend", tags=["AutonomyX"])
async def suspend_autonomyx_agent(agent_id: str):
    """Suspend an AutonomyX agent."""
    from autonomyx_agent import AutonomyXAgentRegistry
    registry = AutonomyXAgentRegistry()
    agent = registry.suspend_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "suspended", "agent_id": agent.agent_id}


@app.post("/autonomyx/agents/{agent_id}/reactivate", tags=["AutonomyX"])
async def reactivate_autonomyx_agent(agent_id: str):
    """Reactivate an AutonomyX agent."""
    from autonomyx_agent import AutonomyXAgentRegistry
    registry = AutonomyXAgentRegistry()
    agent = registry.reactivate_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "active", "agent_id": agent.agent_id}


@app.post("/autonomyx/agents/{agent_id}/rotate-credential", tags=["AutonomyX"])
async def rotate_autonomyx_credential(agent_id: str):
    """Rotate agent credentials."""
    from autonomyx_agent import AutonomyXAgentRegistry
    registry = AutonomyXAgentRegistry()
    credential = registry.rotate_credential(agent_id)
    if not credential:
        raise HTTPException(status_code=404, detail="Agent not found or not active")
    return {"credential_id": credential.credential_id, "token": credential.token, "expires_at": credential.expires_at.isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)