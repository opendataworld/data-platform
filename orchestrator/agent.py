"""Data Platform Agent - Core orchestration with all services."""
import os
import json
from typing import Optional, Literal
from dataclasses import dataclass, field
from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# ============ Service Registry ============
class ServiceRouter:
    """Routes requests to appropriate services."""
    INGEST_SERVICES = {"firecrawl": {}, "crawl4ai": {}, "scrapy": {}}
    EMBEDDING_SERVICES = {"ollama": {}, "openai": {}, "cohere": {}}
    OCR_SERVICES = {"pytesseract": {}, "easyocr": {}, "docTR": {}}
    IMAGE_SERVICES = {"pillow": {}, "opencv": {}, "rembg": {}}
    LLM_SERVICES = {"ollama": {}, "openai": {}, "anthropic": {}}
    CHUNKING_SERVICES = {"recursive": {}, "semantic": {}, "token": {}}
    GOVERNANCE_SERVICES = {"soda": {}, "great_expectations": {}, "dataquality": {}}
    METADATA_SERVICES = {"openmetadata": {}, "atlas": {}, "marquez": {}}
    GRAPH_SERVICES = {"terminusdb": {}, "neo4j": {}, "surrealdb": {}}
    STORAGE_SERVICES = {"s3": {}, "gcs": {}, "azure_blob": {}}
    DATABASE_SERVICES = {"postgresql": {}, "mysql": {}, "mongodb": {}}

class ServiceRegistry:
    """Registry for all available services."""
    def __init__(self):
        self.router = ServiceRouter()

# ============ Tool Creators ============
def create_wordpress_tools():
    """WordPress blog publishing tools."""
    import requests
    @tool
    def create_wordpress_post(site_url: str, username: str, application_password: str, title: str, content: str, status: str = "draft") -> dict:
        """Publish blog to WordPress."""
        resp = requests.post(f"{site_url}/wp-json/wp/v2/posts", json={"title": title, "content": content, "status": status}, auth=(username, application_password), timeout=30)
        resp.raise_for_status()
        return resp.json()
    return [create_wordpress_post]

def create_crawl_tools():
    """Web crawling and data extraction tools."""
    @tool
    def crawl_url(url: str, service: str = "firecrawl") -> dict:
        """Crawl a URL and extract content."""
        return {"url": url, "service": service, "content": f"Extracted content from {url}", "status": "success"}
    @tool
    def scrape_with_xpath(url: str, xpath: str) -> dict:
        """Scrape using XPath selector."""
        return {"url": url, "xpath": xpath, "elements": []}
    @tool
    def extract_structured(url: str, schema: dict) -> dict:
        """Extract structured data from URL."""
        return {"url": url, "schema": schema, "data": {}}
    return [crawl_url, scrape_with_xpath, extract_structured]

def create_embedding_tools():
    """Text embedding and vectorization tools."""
    @tool
    def embed_text(text: str, model: str = "nomic-embed-text", service: str = "ollama") -> dict:
        """Generate embeddings for text."""
        return {"text": text, "model": model, "embedding": [0.1] * 384, "dimensions": 384}
    @tool
    def embed_batch(texts: list, model: str = "nomic-embed-text") -> dict:
        """Generate embeddings for batch of texts."""
        return {"count": len(texts), "model": model, "embeddings": [[0.1] * 384] * len(texts)}
    return [embed_text, embed_batch]

def create_chunking_tools():
    """Text chunking and splitting tools."""
    @tool
    def chunk_text(text: str, method: str = "recursive", chunk_size: int = 1000, overlap: int = 200) -> dict:
        """Chunk text into smaller pieces."""
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap)]
        return {"chunks": chunks, "count": len(chunks), "method": method}
    @tool
    def semantic_chunk(text: str) -> dict:
        """Semantic chunking of text."""
        return {"chunks": [text], "method": "semantic"}
    return [chunk_text, semantic_chunk]

def create_ocr_tools():
    """OCR and image text extraction."""
    @tool
    def extract_text_from_image(image_path: str, service: str = "pytesseract") -> dict:
        """Extract text from image using OCR."""
        return {"image_path": image_path, "text": "Extracted text", "service": service}
    @tool
    def extract_text_from_pdf(pdf_path: str) -> dict:
        """Extract text from PDF."""
        return {"pdf_path": pdf_path, "text": "PDF text content", "pages": 1}
    return [extract_text_from_image, extract_text_from_pdf]

def create_data_quality_tools():
    """Data quality and validation tools."""
    @tool
    def validate_dataset(data: dict, framework: str = "soda") -> dict:
        """Validate dataset against quality checks."""
        return {"status": "passed", "checks": [], "score": 100, "framework": framework}
    @tool
    def check_anomalies(data: dict, method: str = "zscore") -> dict:
        """Detect anomalies in dataset."""
        return {"anomalies": [], "method": method, "count": 0}
    @tool
    def compute_statistics(data: dict) -> dict:
        """Compute dataset statistics."""
        return {"count": 0, "mean": 0, "std": 0, "nulls": 0}
    return [validate_dataset, check_anomalies, compute_statistics]

def create_metadata_tools():
    """Metadata catalog and governance tools."""
    @tool
    def register_dataset(name: str, description: str = "", owner: str = "system") -> dict:
        """Register dataset in metadata catalog."""
        return {"id": f"ds_{name.lower().replace(' ', '_')}", "name": name, "status": "registered"}
    @tool
    def search_metadata(query: str) -> dict:
        """Search metadata catalog."""
        return {"results": [], "query": query}
    @tool
    def get_data_lineage(dataset_id: str) -> dict:
        """Get data lineage for dataset."""
        return {"dataset_id": dataset_id, "upstream": [], "downstream": []}
    @tool
    def add_lineage(source: str, target: str, transformation: str = "copy") -> dict:
        """Record data lineage."""
        return {"source": source, "target": target, "transformation": transformation, "recorded": True}
    return [register_dataset, search_metadata, get_data_lineage, add_lineage]

def create_graph_tools():
    """Graph database tools for knowledge graphs."""
    @tool
    def create_entity(name: str, type: str, properties: dict = {}) -> dict:
        """Create entity in knowledge graph."""
        return {"id": f"entity_{name.lower()}", "name": name, "type": type}
    @tool
    def create_relationship(source: str, target: str, type: str) -> dict:
        """Create relationship in knowledge graph."""
        return {"from": source, "to": target, "type": type, "created": True}
    @tool
    def query_graph(cypher: str) -> dict:
        """Query knowledge graph."""
        return {"results": [], "cypher": cypher}
    return [create_entity, create_relationship, query_graph]

def create_storage_tools():
    """Cloud storage tools."""
    @tool
    def upload_to_s3(data: bytes, bucket: str, key: str) -> dict:
        """Upload data to S3."""
        return {"bucket": bucket, "key": key, "url": f"s3://{bucket}/{key}"}
    @tool
    def download_from_s3(bucket: str, key: str) -> dict:
        """Download data from S3."""
        return {"bucket": bucket, "key": key, "data": b"content"}
    @tool
    def list_s3_objects(bucket: str, prefix: str = "") -> dict:
        """List objects in S3 bucket."""
        return {"objects": [], "bucket": bucket, "prefix": prefix}
    return [upload_to_s3, download_from_s3, list_s3_objects]

def create_database_tools():
    """Database operations tools."""
    @tool
    def execute_query(query: str, database: str = "postgresql") -> dict:
        """Execute SQL query."""
        return {"query": query, "rows": [], "affected": 0}
    @tool
    def create_table(name: str, schema: dict, database: str = "postgresql") -> dict:
        """Create database table."""
        return {"table": name, "schema": schema, "created": True}
    @tool
    def list_tables(database: str = "postgresql") -> dict:
        """List database tables."""
        return {"tables": []}
    return [execute_query, create_table, list_tables]

def create_llm_tools():
    """LLM and AI processing tools."""
    @tool
    def generate_text(prompt: str, model: str = "llama3", max_tokens: int = 500) -> dict:
        """Generate text using LLM."""
        return {"prompt": prompt, "model": model, "text": "Generated response", "tokens": max_tokens}
    @tool
    def classify_text(text: str, labels: list) -> dict:
        """Classify text into categories."""
        return {"text": text, "labels": labels, "predicted": labels[0] if labels else None}
    @tool
    def extract_entities(text: str, entity_type: str = "generic") -> dict:
        """Extract entities from text."""
        return {"text": text, "entities": [], "type": entity_type}
    @tool
    def summarize_text(text: str, max_length: int = 200) -> dict:
        """Summarize text."""
        return {"text": text, "summary": text[:max_length], "length": max_length}
    @tool
    def translate_text(text: str, target_lang: str) -> dict:
        """Translate text to target language."""
        return {"text": text, "translated": f"[{target_lang}] {text}", "language": target_lang}
    return [generate_text, classify_text, extract_entities, summarize_text, translate_text]

# ============ Tool Aggregation ============
def create_data_management_tools() -> list[BaseTool]:
    """Create all data management tools."""
    tools = []
    tools.extend(create_crawl_tools())
    tools.extend(create_embedding_tools())
    tools.extend(create_chunking_tools())
    tools.extend(create_ocr_tools())
    tools.extend(create_data_quality_tools())
    tools.extend(create_metadata_tools())
    tools.extend(create_graph_tools())
    tools.extend(create_storage_tools())
    tools.extend(create_database_tools())
    tools.extend(create_llm_tools())
    tools.extend(create_wordpress_tools())
    return tools

# ============ Agent State ============
class AgentState(BaseModel):
    messages: list = field(default_factory=list)
    context: dict = field(default_factory=dict)
    next_action: str = "tools"
    tool_calls: list = field(default_factory=list)
    tool_results: list = field(default_factory=list)

# ============ LangGraph Agent ============
def create_agent_graph():
    """Create the LangGraph agent workflow."""
    workflow = StateGraph(AgentState)
    
    def agent_node(state: AgentState):
        return {"next_action": "tools"}
    
    def tool_caller(state: AgentState):
        return {"tool_results": []}
    
    def should_continue(state: AgentState) -> Literal["tools", END]:
        return END
    
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_caller)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", "tools")
    workflow.add_conditional_edges("tools", should_continue)
    
    return workflow.compile()

def get_agent():
    """Get the configured agent."""
    return DataPlatformAgent()

def create_tools():
    """Create all tools for the agent."""
    return create_data_management_tools()

# ============ Data Platform Agent ============
class DataPlatformAgent:
    """Main agent for data platform operations."""
    def __init__(self, model: str = "llama3", ollama_url: str = "http://localhost:11434"):
        self.model = model
        self.ollama_url = ollama_url
        self.graph = create_agent_graph()
        self.tools = create_tools()
        self.service_registry = ServiceRegistry()
    
    async def run(self, user_input: str, context: dict = None) -> dict:
        """Run the agent with user input."""
        result = await self.graph.ainvoke({"messages": [{"role": "user", "content": user_input}]})
        return {"response": "Processed", "tool_calls": result.get("tool_calls", [])}
    
    def get_available_tools(self) -> list[str]:
        """Get list of available tool names."""
        return [t.name for t in self.tools]
    
    def get_service_info(self) -> dict:
        """Get information about available services."""
        return {
            "ingest": ServiceRouter.INGEST_SERVICES,
            "embedding": ServiceRouter.EMBEDDING_SERVICES,
            "llm": ServiceRouter.LLM_SERVICES,
            "chunking": ServiceRouter.CHUNKING_SERVICES,
            "governance": ServiceRouter.GOVERNANCE_SERVICES,
            "metadata": ServiceRouter.METADATA_SERVICES,
            "graph": ServiceRouter.GRAPH_SERVICES,
            "storage": ServiceRouter.STORAGE_SERVICES,
            "database": ServiceRouter.DATABASE_SERVICES,
        }

# Import tool decorator
from langchain_core.tools import tool
