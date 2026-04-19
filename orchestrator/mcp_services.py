#!/usr/bin/env python3
"""
MCP Server for Data Platform Services
Exposes data platform services via MCP (Model Context Protocol)
"""
import asyncio
import json
import logging
import sys
from typing import Any, Optional
from pathlib import Path

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Resource,
    SamplingMessage,
)
from mcp.server.llm import LLMProvider, generate_text_or_tool_call
from mcp.shared import MessageStream

# Import service registry
sys.path.insert(0, str(Path(__file__).parent))
from agent import ServiceRegistry, create_data_management_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("data-platform-mcp")


def create_mcp_tools():
    """Create MCP tools from ServiceRegistry."""
    
    tools = [
        # --- Crawling ---
        Tool(
            name="crawl_url",
            description="Crawl a URL and extract content using web scraping services like jina-reader, trafilatura, firecrawl",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to crawl"},
                    "service": {
                        "type": "string",
                        "description": f"Service to use: {', '.join(ServiceRegistry.CRAWL[:3])}...",
                        "default": "jina-reader"
                    }
                },
                "required": ["url"]
            }
        ),
        # --- Embedding ---
        Tool(
            name="embed_text",
            description="Create embeddings for text using various embedding models",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to embed"},
                    "service": {
                        "type": "string",
                        "description": f"Service: {', '.join(ServiceRegistry.EMBEDDING[:3])}...",
                        "default": "sentence-transformers"
                    }
                },
                "required": ["text"]
            }
        ),
        # --- Chunking ---
        Tool(
            name="chunk_text",
            description="Chunk text into smaller pieces",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to chunk"},
                    "method": {
                        "type": "string",
                        "description": f"Method: {', '.join(ServiceRegistry.CHUNKING[:3])}",
                        "default": "recursive"
                    },
                    "chunk_size": {"type": "integer", "default": 1000}
                },
                "required": ["text"]
            }
        ),
        # --- OCR ---
        Tool(
            name="run_ocr",
            description="Run OCR on an image to extract text",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "Path to image file"},
                    "service": {
                        "type": "string",
                        "description": f"Service: {', '.join(ServiceRegistry.OCR[:3])}",
                        "default": "tesseract"
                    }
                },
                "required": ["image_path"]
            }
        ),
        # --- Speech-to-Text ---
        Tool(
            name="transcribe_audio",
            description="Transcribe audio to text using speech recognition",
            inputSchema={
                "type": "object",
                "properties": {
                    "audio_path": {"type": "string", "description": "Path to audio file"},
                    "service": {"type": "string", "default": "whisper"}
                },
                "required": ["audio_path"]
            }
        ),
        # --- LLM ---
        Tool(
            name="query_llm",
            description="Query a language model",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Prompt for the LLM"},
                    "model": {
                        "type": "string",
                        "description": f"Model: {', '.join(ServiceRegistry.LLM[:3])}",
                        "default": "llama3"
                    }
                },
                "required": ["prompt"]
            }
        ),
        # --- Image Generation ---
        Tool(
            name="generate_image",
            description="Generate an image from text prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Text prompt"},
                    "service": {
                        "type": "string",
                        "description": "Image service",
                        "default": "diffusers"
                    }
                },
                "required": ["prompt"]
            }
        ),
        # --- Clustering ---
        Tool(
            name="run_clustering",
            description="Run clustering on vectors",
            inputSchema={
                "type": "object",
                "properties": {
                    "vectors": {"type": "array", "description": "List of vectors"},
                    "method": {"type": "string", "default": "kmeans"},
                    "n_clusters": {"type": "integer", "default": 5}
                },
                "required": ["vectors"]
            }
        ),
        # --- Data Quality ---
        Tool(
            name="validate_data",
            description="Validate data quality",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Data source to validate"},
                    "framework": {
                        "type": "string",
                        "description": f"Framework: {', '.join(ServiceRegistry.QUALITY[:3])}",
                        "default": "great-expectations"
                    }
                },
                "required": ["source"]
            }
        ),
        # --- Data Lineage ---
        Tool(
            name="check_lineage",
            description="Check data lineage",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset": {"type": "string", "description": "Data asset"},
                    "framework": {"type": "string", "default": "marquez"}
                },
                "required": ["asset"]
            }
        ),
        # --- Workflow Orchestration ---
        Tool(
            name="orchestrate_workflow",
            description="Orchestrate data workflow",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {"type": "string", "description": "Workflow name"},
                    "tool": {
                        "type": "string",
                        "description": f"Tool: {', '.join(ServiceRegistry.ORCHESTRATION[:3])}",
                        "default": "airflow"
                    }
                },
                "required": ["workflow"]
            }
        ),
        # --- Data Streaming ---
        Tool(
            name="stream_data",
            description="Publish to data stream",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic name"},
                    "service": {"type": "string", "default": "kafka"}
                },
                "required": ["topic"]
            }
        ),
        # --- Data Transfer ---
        Tool(
            name="transfer_data",
            description="Transfer data between systems",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Source location"},
                    "destination": {"type": "string", "description": "Destination location"},
                    "service": {"type": "string", "default": "rclone"}
                },
                "required": ["source", "destination"]
            }
        ),
        # --- Data Integration ---
        Tool(
            name="integrate_data",
            description="Integrate data from sources",
            inputSchema={
                "type": "object",
                "properties": {
                    "sources": {"type": "array", "description": "Source list"},
                    "target": {"type": "string", "description": "Target location"},
                    "service": {"type": "string", "default": "trino"}
                },
                "required": ["sources", "target"]
            }
        ),
        # --- NER ---
        Tool(
            name="extract_entities",
            description="Extract named entities",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to extract from"},
                    "service": {"type": "string", "default": "spacy-ner"}
                },
                "required": ["text"]
            }
        ),
        # --- PII Detection ---
        Tool(
            name="detect_pii",
            description="Detect PII in text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to analyze"},
                    "service": {"type": "string", "default": "presidio-analyzer"}
                },
                "required": ["text"]
            }
        ),
        # --- Taxonomy Classification ---
        Tool(
            name="classify_taxonomy",
            description="Classify text into taxonomy",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to classify"},
                    "taxonomy": {"type": "string", "default": "iptc-media-topics"}
                },
                "required": ["text"]
            }
        ),
        # --- Entity Resolution ---
        Tool(
            name="resolve_entities",
            description="Resolve entities to knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text with entities"},
                    "service": {"type": "string", "default": "entity-resolution"}
                },
                "required": ["text"]
            }
        ),
        # --- List Services ---
        Tool(
            name="list_services",
            description="List available services by category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category: crawl, embedding, llm, quality, governance, etc."
                    }
                }
            }
        ),
        # --- Get Service Info ---
        Tool(
            name="get_service_info",
            description="Get detailed information about services",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]
    
    return tools


# Register tools with server
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return create_mcp_tools()


@server.call_tool()
async def call_tool(
    name: str,
    arguments: dict | None
) -> list[TextContent] | list[ImageContent] | list[EmbeddedResource]:
    """Handle tool calls."""
    
    args = arguments or {}
    logger.info(f"Tool called: {name} with args: {args}")
    
    # Info tools
    if name == "get_service_info":
        from agent import ServiceRegistry
        info = {
            "data_engineering": ServiceRegistry.ORCHESTRATION + ServiceRegistry.STREAMING,
            "data_transfer": ServiceRegistry.TRANSFER,
            "data_integration": ServiceRegistry.ETL,
            "data_quality": ServiceRegistry.QUALITY,
            "data_governance": ServiceRegistry.GOVERNANCE,
            "crawling": ServiceRegistry.CRAWL,
            "embedding": ServiceRegistry.EMBEDDING,
            "llm": ServiceRegistry.LLM,
            "ocr": ServiceRegistry.OCR,
            "nlp": ServiceRegistry.NLP,
            "entity_resolution": ServiceRegistry.ENTITY_RESOLUTION,
            "chunking": ServiceRegistry.CHUNKING,
            "vector": ServiceRegistry.VECTOR,
            "clustering": ServiceRegistry.CLUSTERING,
            "workflow": ServiceRegistry.WORKFLOW,
        }
        return [TextContent(type="text", text=json.dumps(info, indent=2))]
    
    if name == "list_services":
        category = args.get("category", "")
        from agent import ServiceRegistry
        
        cat_map = {
            "crawl": ServiceRegistry.CRAWL,
            "embedding": ServiceRegistry.EMBEDDING,
            "llm": ServiceRegistry.LLM,
            "quality": ServiceRegistry.QUALITY,
            "governance": ServiceRegistry.GOVERNANCE,
            "orchestration": ServiceRegistry.ORCHESTRATION,
            "streaming": ServiceRegistry.STREAMING,
            "transfer": ServiceRegistry.TRANSFER,
            "integration": ServiceRegistry.ETL,
            "nlp": ServiceRegistry.NLP,
            "chunking": ServiceRegistry.CHUNKING,
            "vector": ServiceRegistry.VECTOR,
            "clustering": ServiceRegistry.CLUSTERING,
        }
        
        result = cat_map.get(category, list(cat_map.values())[0])
        return [TextContent(type="text", text=json.dumps(result))]
    
    # Generic service response
    result = {
        "tool": name,
        "args": args,
        "status": "ready",
        "message": f"Would execute {name} with {args}"
    }
    
    return [TextContent(type="text", text=json.dumps(result, default=str))]


async def main():
    """Main entry point."""
    logger.info("Starting Data Platform MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())