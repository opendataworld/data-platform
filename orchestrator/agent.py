"""
LangGraph Orchestrator Agent using open-source LLM (Ollama/Llama)
Manages all data platform services through a unified agent interface.
With AutonomyX Agent Identity Specification v1.0
"""
from typing import TypedDict, Literal, Sequence
from datetime import datetime
import logging
import os

from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import BaseTool, tool

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# AutonomyX imports
from autonomyx_agent import (
    AutonomyXAgentRegistry, 
    DataPlatformAgentFactory,
    AgentCreateRequest,
    AgentDetail,
    BudgetPolicy,
    RatePolicy
)

# Billing imports
#from billing import # object , SERVICE_PRICING, ServiceUsageTracker

logger = logging.getLogger(__name__)


# ==== SERVICE REGISTRY ====

class ServiceRegistry:
    """
    Complete registry of all data platform services organized by category.
    Based on IBM Data Management Guide categories.
    """
    
    # --- IBM Data Management Guide Topics ---
    
    # DATA PLATFORMS
    DATA_WAREHOUSE = ["postgres", "clickhouse", "trino"]
    DATA_LAKE = ["s3", "minio", "datalake"]
    LAKEHOUSE = ["databricks-lakehouse"]
    
    # DATA ARCHITECTURE (catalogs already covered)
    DATA_CATALOGS = ["datahub", "amundsen", "atlas", "collibra", "openmetadata"]
    
    # DATA ENGINEERING
    ORCHESTRATION = ["airflow", "dagster", "prefect", "temporal"]
    STREAMING = ["kafka", "redpanda", "pulsar"]
    
    # DATA TRANSFER / MOVEMENT
    TRANSFER = ["rclone", "airbyte", "meltano", "debezium"]
    
    # DATA INTEGRATION
    ETL = ["trino", "duckdb", "apache-pinot", "glue"]
    
    # DATA QUALITY
    QUALITY = ["great-expectations", "soda-core", "ydata-profiling", "pandas-profiling"]
    
    # DATA GOVERNANCE
    GOVERNANCE = ["datahub", "amundsen", "atlas", "collibra", "openmetadata", "marquez"]
    
    # DATA DEMOCRATIZATION
    DEMOCRATIZATION = ["data-catalog-democratization", "openmetadata"]
    
    # DATA OPTIMIZATION / REDUCTION
    OPTIMIZATION = ["data-optimization", "data-reduction", "pyarrow"]
    
    # --- ML/AI Services ---
    
    # Crawling/Ingestion
    CRAWL = ["firecrawl", "crawl4ai", "playwright", "jina-reader", "trafilatura", "unstructured", "grobid"]
    
    # Embeddings
    EMBEDDING = ["sentence-transformers", "word2vec", "fasttext", "bge-embeddings", "e5-embeddings", "gpt-embedding", "cohere", "instructor-embeddings"]
    
    # OCR/Speech
    OCR = ["tesseract", "easyocr", "paddleocr", "whisper", "faster-whisper", "coqui-stt"]
    
    # Image/Video AI
    IMAGE = ["timm", "clip", "transformers-vision", "sam", "blip", "detr", "grounding-dino", "opencv", "yolo"]
    VIDEO_GEN = ["diffusers", "stable-diffusion", "modelscope-t2v", "zeroscope", "animate-anything"]
    
    # LLMs
    LLM = ["ollama", "gpt4all", "text-generation-webui", "huggingface-transformers"]
    
    # NLP
    NLP = ["spacy-ner", "presidio-analyzer", "opennlp", "flair"]
    ENTITY_RESOLUTION = ["entity-resolution", "wink", "relik"]
    
    # Chunking
    CHUNKING = ["langchain-text-splitters", "chunking", "semantic-chunker", "markdown-splitter"]
    
    # Vector Search
    VECTOR = ["faiss", "annoy", "hnswlib", "qdrant", "weaviate"]
    
    # Clustering
    CLUSTERING = ["clustering", "pyclustering", "bertopic"]
    
    # Unstructured to Structured
    U2S = ["llamaindex", "document-intelligence", "table-extractor", "selectorlib", "text-extract"]
    
    # Low-Code/No-Code Workflow
    WORKFLOW = ["langflow", "n8n", "flowise", "promptly", "chainlit"]
    
    @classmethod
    def get_services(cls, category: str) -> list[str]:
        """Get services by category name."""
        return getattr(cls, category.upper(), [])
    
    @classmethod
    def get_category(cls, service: str) -> str:
        """Get category for a service."""
        for cat in dir(cls):
            if cat.startswith('_'):
                continue
            if service in getattr(cls, cat):
                return cat.lower()
        return "unknown"


def create_data_management_tools() -> list[BaseTool]:
    """Create tools aligned with IBM Data Management Guide topics."""
    
    @tool
    def data_quality_check(source: str, framework: str = "great-expectations") -> dict:
        """
        Check data quality - validate accuracy, completeness, consistency.
        Topics: Data quality, Data governance
        """
        available = ServiceRegistry.QUALITY
        if framework not in available:
            framework = available[0]
        return {
            "framework": framework,
            "source": source,
            "checks": ["accuracy", "completeness", "consistency", "uniqueness", "timeliness"],
            "status": "ready"
        }
    
    @tool
    def data_profiling(source: str, framework: str = "ydata-profiling") -> dict:
        """
        Profile data - generate statistical summaries and insights.
        Topic: Data quality
        """
        available = ["ydata-profiling", "pandas-profiling"]
        if framework not in available:
            framework = available[0]
        return {"framework": framework, "source": source, "status": "ready"}
    
    @tool
    def orchestrate_workflow(workflow: str, tool: str = "airflow") -> dict:
        """
        Orchestrate data workflows/pipelines.
        Topic: Data engineering
        """
        available = ServiceRegistry.ORCHESTRATION
        if tool not in available:
            tool = available[0]
        return {"workflow": workflow, "tool": tool, "status": "ready"}
    
    @tool
    def stream_data(topic: str, service: str = "kafka") -> dict:
        """
        Process data streams - real-time event processing.
        Topic: Data processing (streaming)
        """
        available = ServiceRegistry.STREAMING
        if service not in available:
            service = available[0]
        return {"topic": topic, "service": service, "status": "ready"}
    
    @tool
    def transfer_data(source: str, destination: str, service: str = "rclone") -> dict:
        """
        Transfer data between systems/cloud storage.
        Topic: Data transfer
        """
        available = ServiceRegistry.TRANSFER
        if service not in available:
            service = available[0]
        return {"source": source, "destination": destination, "service": service, "status": "ready"}
    
    @tool
    def integrate_data(sources: list, target: str, service: str = "trino") -> dict:
        """
        Integrate data from multiple sources.
        Topic: Data integration
        """
        available = ServiceRegistry.ETL
        if service not in available:
            service = available[0]
        return {"sources": sources, "target": target, "service": service, "status": "ready"}
    
    @tool
    def optimize_data(source: str, service: str = "data-optimization") -> dict:
        """
        Optimize data - improve performance, reduce size.
        Topic: Data optimization
        """
        available = ServiceRegistry.OPTIMIZATION
        return {"source": source, "service": service, "status": "ready"}
    
    @tool
    def consolidate_data(sources: list, service: str = "data-consolidation") -> dict:
        """
        Consolidate data from silos.
        Topic: Data silos
        """
        return {"sources": sources, "service": service, "status": "ready"}
    
    @tool
    def democratize_data(service: str = "data-catalog-democratization") -> dict:
        """
        Make data accessible across organization.
        Topic: Data democratization
        """
        return {"service": service, "status": "ready"}
    
    @tool
    def monitor_data_sla(metrics: list, service: str = "data-sla") -> dict:
        """
        Monitor data SLA - availability, freshness, quality metrics.
        Topic: Data SLA
        """
        return {"metrics": metrics, "service": service, "status": "ready"}
    
    @tool
    def govern_data(policy: str, service: str = "datahub") -> dict:
        """
        Apply data governance policies.
        Topics: Data governance, Enterprise data management
        """
        available = ServiceRegistry.GOVERNANCE
        if service not in available:
            service = available[0]
        return {"policy": policy, "service": service, "status": "ready"}
    
    @tool
    def check_data_lineage(asset: str, service: str = "marquez") -> dict:
        """
        Track data lineage - provenance and transformation history.
        Topic: Enterprise data management
        """
        return {"asset": asset, "service": service, "status": "ready"}
    
    # --- Existing ML/AI tools wrapped with ServiceRegistry ---
    
    @tool
    def crawl_and_extract(url: str, service: str = "jina-reader") -> dict:
        """Crawl a URL and extract content."""
        if service not in ServiceRegistry.CRAWL:
            service = ServiceRegistry.CRAWL[0]
        return {"url": url, "service": service, "status": "ready"}
    
    @tool
    def embed_text(text: str, service: str = "sentence-transformers") -> dict:
        """Create embeddings for text."""
        if service not in ServiceRegistry.EMBEDDING:
            service = ServiceRegistry.EMBEDDING[0]
        return {"service": service, "text": text[:100], "status": "ready"}
    
    @tool
    def query_llm(prompt: str, model: str = "llama3") -> str:
        """Query the LLM."""
        if model not in ServiceRegistry.LLM:
            model = ServiceRegistry.LLM[0]
        return f"Would query {model} with: {prompt[:50]}..."

    # --- Billing tools ---
    
    @tool
    def get_service_pricing(service_id: str) -> dict:
        """Get pricing for a service."""
        #from billing import SERVICE_PRICING
        pricing = SERVICE_PRICING.get(service_id)
        if pricing:
            return {
                "service_id": pricing.service_id,
                "service_name": pricing.service_name,
                "unit_price_cents": pricing.unit_price_cents,
                "unit": pricing.unit,
                "monthly_price_cents": pricing.monthly_price_cents
            }
        return {"error": "Service not found"}
    
    @tool
    def list_all_pricing() -> dict:
        """List all service pricing."""
        #from billing import SERVICE_PRICING
        return [{"service_id": sp.service_id, "service_name": sp.service_name, "unit_price_cents": sp.unit_price_cents, "unit": sp.unit, "monthly_price_cents": sp.monthly_price_cents} for sp in SERVICE_PRICING.values()]
    
    @tool
    def create_customer(customer_id: str, name: str, email: str) -> dict:
        """Create a customer in the billing system."""
        #from billing import LagoBillingClient
        client = LagoBillingClient()
        return client.create_customer(customer_id, name, email)
    
    @tool
    def track_usage(customer_id: str, service_id: str, quantity: float) -> dict:
        """Track service usage for billing."""
        #from billing import ServiceUsageTracker
        tracker = ServiceUsageTracker()
        return tracker.track_usage(customer_id, service_id, quantity)
    
    @tool
    def get_billing_summary(customer_id: str) -> dict:
        """Get billing summary for a customer."""
        #from billing import ServiceUsageTracker
        tracker = ServiceUsageTracker()
        return tracker.get_customer_usage(customer_id)
    
    return [
        data_quality_check,
        data_profiling,
        orchestrate_workflow,
        stream_data,
        transfer_data,
        integrate_data,
        optimize_data,
        consolidate_data,
        democratize_data,
        monitor_data_sla,
        govern_data,
        check_data_lineage,
        crawl_and_extract,
        embed_text,
        query_llm,
        get_service_pricing,
        list_all_pricing,
        create_customer,
        track_usage,
        get_billing_summary,
    ]


# ==== AGENT GRAPH ====

def create_agent_graph():
    """Create the LangGraph agent."""
    from langgraph.graph import StateGraph, END
    
    class AgentState(TypedDict):
        messages: list
        context: dict
        last_action: str | None
        tools_used: list
        results: dict
        error: str | None
    
    tools = create_data_management_tools()
    tool_node = ToolNode(tools)
    
    SYSTEM_PROMPT = """You are a data platform orchestrator agent.
    
    You manage services aligned with the IBM Data Management Guide:
    
    **Data Platforms**: Snowflake, Databricks, BigQuery, Postgres
    **Data Architecture**: Data catalogs (DataHub, Amundsen, Atlas)
    **Data Engineering**: Airflow, Dagster, Prefect, Temporal
    **Data Transfer**: rclone, Airbyte, Meltano
    **Data Integration**: Trino, DuckDB, Apache Pinot
    **Data Quality**: Great Expectations, Soda Core, YData Profiling
    **Data Governance**: DataHub, Atlas, Collibra, OpenMetadata, Marquez
    **Data Democratization**: Open Metadata, data catalogs
    **Data Optimization**: PyArrow, compression
    **Data SLA**: Prometheus monitoring
    
    Plus ML/AI services:
    - Crawling: Firecrawl, Crawl4ai, Jina Reader
    - Embeddings: Sentence-transformers, BGE, E5
    - OCR: Tesseract, EasyOCR, Whisper
    - Image AI: CLIP, SAM, BLIP, YOLO
    - LLMs: Ollama, GPT4All
    - NLP: spaCy NER, Presidio
    - Entity Resolution: spaCy linker, WINK
    
    Use tools from appropriate services to help users."""
    
    def agent_node(state: AgentState):
        """Main agent node."""
        from langchain_openai import ChatOllama
        
        llm = ChatOllama(
            model=os.getenv("LLM_MODEL", "llama3"),
            base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
            temperature=0.7
        )
        
        llm_with_tools = llm.bind_tools(tools)
        messages = state.get("messages", [])
        response = llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def tool_caller(state: AgentState):
        """Call tools based on agent response."""
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return {"tools_used": [tc["name"] for tc in last_message.tool_calls]}
        
        return {"tools_used": []}
    
    def should_continue(state: AgentState) -> Literal["tools", END]:
        """Determine if we should continue."""
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END
    
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_caller)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    
    return graph.compile()


def get_agent():
    """Get the compiled agent."""
    return create_agent_graph()


# ==== MAIN AGENT CLASS ====

#class DataPlatformAgent( object ):
    """Main orchestrator agent for the data platform with AutonomyX and Billing."""
    
    def __init__(self, model: str = "llama3", ollama_url: str = "http://localhost:11434",
                 autonomyx_registry: AutonomyXAgentRegistry = None):
        self.model = model
        self.ollama_url = ollama_url
        self.graph = get_agent()
        self.tools = create_data_management_tools()
        self.registry = ServiceRegistry()
        
        # AutonomyX integration
        self.autonomyx_registry = autonomyx_registry or AutonomyXAgentRegistry()
        self.agent_factory = DataPlatformAgentFactory(self.autonomyx_registry)
        self.current_agent: AgentDetail = None
    
    async def run(self, user_input: str, context: dict = None) -> dict:
        """Run the agent with user input."""
        from langchain_core.messages import HumanMessage
        
        messages = [HumanMessage(content=user_input)]
        state = {
            "messages": messages,
            "context": context or {},
            "last_action": None,
            "tools_used": [],
            "results": {},
            "error": None
        }
        
        result = await self.graph.ainvoke(state)
        return result
    
    def get_available_tools(self) -> list[str]:
        """Get list of available tools."""
        return [t.name for t in self.tools]
    
    def get_service_info(self) -> dict:
        """Get information about available services."""
        return {
            "data_quality": ServiceRegistry.QUALITY,
            "orchestration": ServiceRegistry.ORCHESTRATION,
            "streaming": ServiceRegistry.STREAMING,
            "transfer": ServiceRegistry.TRANSFER,
            "integration": ServiceRegistry.ETL,
            "governance": ServiceRegistry.GOVERNANCE,
            "catalogs": ServiceRegistry.DATA_CATALOGS,
            "crawl": ServiceRegistry.CRAWL,
            "embedding": ServiceRegistry.EMBEDDING,
            "llm": ServiceRegistry.LLM,
            "ocr": ServiceRegistry.OCR,
            "image": ServiceRegistry.IMAGE,
            "nlp": ServiceRegistry.NLP,
            "chunking": ServiceRegistry.CHUNKING,
            "workflow": ServiceRegistry.WORKFLOW,
        }
    
    # ==== AutonomyX Methods ====
    
    def register_with_autonomyx(self, agent_name: str, sponsor_id: str, 
                                tenant_id: str) -> AgentDetail:
        """Register this agent with AutonomyX."""
        self.current_agent = self.agent_factory.create_orchestrator_agent(
            name=agent_name,
            sponsor_id=sponsor_id,
            tenant_id=tenant_id
        )
        return self.current_agent
    
    def get_autonomyx_agent(self) -> AgentDetail:
        """Get current AutonomyX agent details."""
        return self.current_agent
    
    def list_agents(self, tenant_id: str = None) -> list:
        """List all registered agents."""
        return self.autonomyx_registry.list_agents(tenant_id=tenant_id)
    
    def suspend_agent(self, agent_id: str) -> AgentDetail:
        """Suspend an agent."""
        return self.autonomyx_registry.suspend_agent(agent_id)
    
    def reactivate_agent(self, agent_id: str) -> AgentDetail:
        """Reactivate a suspended agent."""
        return self.autonomyx_registry.reactivate_agent(agent_id)
    
    def revoke_agent(self, agent_id: str) -> AgentDetail:
        """Revoke an agent."""
        return self.autonomyx_registry.revoke_agent(agent_id)
    
    def rotate_credentials(self, agent_id: str):
        """Rotate agent credentials."""
        return self.autonomyx_registry.rotate_credential(agent_id)


if __name__ == "__main__":
    print("Data Platform LangGraph Orchestrator Agent")
    print("=" * 50)
    
    agent = DataPlatformAgent()
    print(f"Available tools ({len(agent.get_available_tools())}):")
    for tool in agent.get_available_tools():
        print(f"  - {tool}")
    
    print(f"\nService categories:")
    info = agent.get_service_info()
    for category, services in info.items():
        print(f"  {category}: {services}")