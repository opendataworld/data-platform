# Data Platform API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health
```bash
GET /health
```

### Services
```bash
GET /services
```

### Crawling
```bash
POST /crawl/extract
{
  "url": "https://example.com",
  "service": "jina-reader"
}
```

### Embedding
```bash
POST /embed/text
{
  "text": "Hello world",
  "service": "sentence-transformers",
  "model": "all-MiniLM-L6-v2"
}
```

### LLM Query
```bash
POST /llm/query
{
  "prompt": "What is data governance?",
  "model": "llama3"
}
```

### Data Quality
```bash
POST /quality/check
{
  "source": "s3://bucket/data.csv",
  "framework": "great-expectations"
}
```

## AutonomyX Agent Management

### Create Agent
```bash
POST /autonomyx/agents
{
  "agent_name": "my-agent",
  "sponsor_subject_id": "user-001",
  "tenant_id": "tenant-001",
  "allowed_models": ["llama3"],
  "max_spend_cents": 50000,
  "max_requests": 1000
}
```

### List Agents
```bash
GET /autonomyx/agents?tenant_id=tenant-001
```

### Suspend Agent
```bash
POST /autonomyx/agents/{agent_id}/suspend
```

### Reactivate Agent
```bash
POST /autonomyx/agents/{agent_id}/reactivate
```

### Rotate Credentials
```bash
POST /autonomyx/agents/{agent_id}/rotate-credential
```

## Service Categories

### Crawling Services
- jina-reader
- firecrawl
- trafilatura
- playwright

### Embedding Services  
- sentence-transformers
- bge
- e5
- word2vec

### LLM Services
- ollama
- gpt4all
- text-generation-webui

### Quality Services
- great-expectations
- soda-core
- ydata-profiling

### Governance Services
- datahub
- atlas
- openmetadata
- marquez