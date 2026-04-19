"""
MCP Server for Data Platform Orchestrator
Exposes data platform services via MCP (Model Context Protocol)
"""
from typing import Any, Literal
from dataclasses import dataclass, field
import logging
import json
import os

# MCP imports - using the reference implementation
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

from agent import DataPlatformAgent, ServiceRouter, create_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# MCP Server
def create_mcp_server():
    """Create an MCP server for the data platform."""
    
    # Create the server
    server = Server("data-platform-orchestrator")
    
    # Get tools
    tools = create_tools()
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="crawl_and_extract",
                description="Crawl a URL and extract content using web scraping services",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to crawl"},
                        "service": {
                            "type": "string",
                            "description": "Service to use: jina-reader, trafilatura, firecrawl, crawl4ai",
                            "default": "jina-reader"
                        }
                    },
                    "required": ["url"]
                }
            ),
            Tool(
                name="embed_text",
                description="Create embeddings for text using various embedding models",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to embed"},
                        "service": {
                            "type": "string",
                            "description": "Embedding service: sentence-transformers, bge, e5, word2vec, fasttext",
                            "default": "sentence-transformers"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="chunk_text",
                description="Chunk text into smaller pieces using various chunking strategies",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to chunk"},
                        "method": {
                            "type": "string",
                            "description": "Chunking method: recursive, semantic, token-based, markdown",
                            "default": "recursive"
                        },
                        "chunk_size": {"type": "integer", "default": 1000}
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="run_ocr",
                description="Run OCR on an image to extract text",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_path": {"type": "string", "description": "Path to image file"},
                        "service": {
                            "type": "string",
                            "description": "OCR service: tesseract, easyocr, paddleocr",
                            "default": "tesseract"
                        }
                    },
                    "required": ["image_path"]
                }
            ),
            Tool(
                name="transcribe_audio",
                description="Transcribe audio to text using speech recognition",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_path": {"type": "string", "description": "Path to audio file"},
                        "service": {
                            "type": "string",
                            "description": "STT service: whisper, faster-whisper, coqui-stt",
                            "default": "whisper"
                        }
                    },
                    "required": ["audio_path"]
                }
            ),
            Tool(
                name="generate_image",
                description="Generate an image from text prompt",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Text prompt for generation"},
                        "service": {
                            "type": "string",
                            "description": "Image generation service: diffusers, stable-diffusion",
                            "default": "diffusers"
                        }
                    },
                    "required": ["prompt"]
                }
            ),
            Tool(
                name="query_llm",
                description="Query a language model",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Prompt for the LLM"},
                        "model": {
                            "type": "string",
                            "description": "Model to use: llama3, mistral, phi",
                            "default": "llama3"
                        }
                    },
                    "required": ["prompt"]
                }
            ),
            Tool(
                name="run_clustering",
                description="Run clustering on vector embeddings",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "vectors": {"type": "array", "description": "List of vectors to cluster"},
                        "method": {
                            "type": "string",
                            "description": "Clustering method: kmeans, dbscan, bertopic",
                            "default": "kmeans"
                        },
                        "n_clusters": {"type": "integer", "default": 5}
                    },
                    "required": ["vectors"]
                }
            ),
            Tool(
                name="validate_data",
                description="Validate data quality",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Data source to validate"},
                        "framework": {
                            "type": "string",
                            "description": "Framework: great-expectations, soda-core",
                            "default": "great-expectations"
                        }
                    },
                    "required": ["source"]
                }
            ),
            Tool(
                name="check_lineage",
                description="Check data lineage",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "asset": {"type": "string", "description": "Data asset to check"},
                        "framework": {
                            "type": "string",
                            "description": "Framework: Marquez, DataHub, Atlas",
                            "default": "marquez"
                        }
                    },
                    "required": ["asset"]
                }
            ),
            Tool(
                name="extract_entities",
                description="Extract named entities from text",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to extract from"},
                        "service": {
                            "type": "string",
                            "description": "NER service: spacy-ner, presidio",
                            "default": "spacy-ner"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="detect_pii",
                description="Detect personally identifiable information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to analyze"},
                        "service": {
                            "type": "string",
                            "description": "PII detection service: presidio-analyzer",
                            "default": "presidio-analyzer"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="classify_taxonomy",
                description="Classify text into a taxonomy",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to classify"},
                        "taxonomy": {
                            "type": "string",
                            "description": "Taxonomy: iptc-media-topics, google-product-taxonomy, iab-taxonomy",
                            "default": "iptc-media-topics"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="list_services",
                description="List available services by category",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Service category: ingest, embedding, ocr, image, llm, chunking, governance"
                        }
                    }
                }
            ),
            Tool(
                name="get_service_info",
                description="Get information about available services",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(
        name: str,
        arguments: dict | None
    ) -> list[TextContent] | list[ImageContent] | list[EmbeddedResource]:
        """Handle tool calls."""
        
        # Get service info
        if name == "get_service_info":
            router = ServiceRouter()
            info = {
                "ingest_services": router.INGEST_SERVICES,
                "embedding_services": router.EMBEDDING_SERVICES,
                "ocr_services": router.OCR_SERVICES,
                "image_services": router.IMAGE_SERVICES,
                "llm_services": router.LLM_SERVICES,
                "chunking_services": router.CHUNKING_SERVICES,
                "governance_services": router.GOVERNANCE_SERVICES,
                "vector_services": router.VECTOR_SERVICES,
                "clustering_services": router.CLUSTERING_SERVICES
            }
            return [TextContent(type="text", text=json.dumps(info, indent=2))]
        
        if name == "list_services":
            category = arguments.get("category", "")
            router = ServiceRouter()
            
            if category == "ingest":
                return [TextContent(type="text", text=json.dumps(router.INGEST_SERVICES))]
            elif category == "embedding":
                return [TextContent(type="text", text=json.dumps(router.EMBEDDING_SERVICES))]
            elif category == "ocr":
                return [TextContent(type="text", text=json.dumps(router.OCR_SERVICES))]
            elif category == "image":
                return [TextContent(type="text", text=json.dumps(router.IMAGE_SERVICES))]
            elif category == "llm":
                return [TextContent(type="text", text=json.dumps(router.LLM_SERVICES))]
            elif category == "chunking":
                return [TextContent(type="text", text=json.dumps(router.CHUNKING_SERVICES))]
            elif category == "governance":
                return [TextContent(type="text", text=json.dumps(router.GOVERNANCE_SERVICES))]
            else:
                return [TextContent(type="text", text="Invalid category")]
        
        # Get the tool
        tool = next((t for t in tools if t.name == name), None)
        if not tool:
            return [TextContent(type="text", text=f"Tool {name} not found")]
        
        # Invoke the tool
        try:
            result = tool.invoke(arguments or {})
            return [TextContent(type="text", text=json.dumps(result, default=str))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return server


async def main():
    """Main entry point for MCP server."""
    server = create_mcp_server()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())