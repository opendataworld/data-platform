# Docker Compose Profiles

## What are Profiles?

Docker Compose profiles allow you to define optional groups of services. Services with profiles are only started when explicitly selected.

## Available Profiles in Data Platform

### 1. `ingest` - Data Ingestion & Crawling
Services for data ingestion, crawling, and initial processing:
- jina-reader, firecrawl, playwright
- trafilatura, unstructured, grobid
- rclone, airbyte, meltano
- LangFlow, n8n, flowise

### 2. `ml` - ML/AI Services
Machine learning and AI services:
- sentence-transformers, bge, e5 embeddings
- tesseract, easyocr, paddleocr (OCR)
- whisper, faster-whisper (Speech)
- ollama, gpt4all (LLMs)
- timm, clip, yolo (Vision)
- airflow, dagster, prefect (Orchestration)

### 3. `store` - Data Stores
Database and storage services:
- postgres, surrealdb
- qdrant, weaviate (Vector DB)
- redis

### 4. `catalog` - Data Catalogs
Metadata and governance catalogs:
- datahub, amundsen, atlas
- collibra, openmetadata
- marquez (lineage)

## How to Use Profiles

### Start specific profile
```bash
# Start only ingestion services
docker-compose --profile ingest up -d

# Start only ML services
docker-compose --profile ml up -d
```

### Start multiple profiles
```bash
# Start ingestion + ML
docker-compose --profile ingest --profile ml up -d
```

### Start everything
```bash
# Start all services (no profile needed)
docker-compose up -d
```

## Profile Usage Examples

### Development (minimal)
```bash
docker-compose --profile store up -d
```
Starts: postgres, redis, ollama

### Data Ingestion Pipeline
```bash
docker-compose --profile ingest up -d
```
Starts: crawlers, LangFlow, n8n, quality tools

### Full ML Platform
```bash
docker-compose --profile ml up -d
```
Starts: All ML/AI services, orchestrators

### Production (all)
```bash
docker-compose up -d
```
Starts: All services

## Service Profile Mapping

| Service | Profiles |
|---------|----------|
| postgres | store, ingest, ml, catalog |
| redis | store, ingest, ml |
| ollama | ml |
| jina-reader | ingest |
| firecrawl | ingest |
| langflow | ingest, ml |
| n8n | ingest, ml |
| airflow | ingest, ml |
| datahub | catalog |
| great-expectations | ingest, ml |

## Quick Reference

```bash
# List available profiles
docker-compose config --profiles

# See which services will start
docker-compose --profile ingest config

# Stop all services in a profile
docker-compose --profile ingest down
```