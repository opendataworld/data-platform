# Coolify Deployment Configuration for Data Platform

## Overview
This configuration allows deploying the Data Platform to Coolify with open-data.world domain.

## Domain Configuration

| Service | URL | Coolify Resource |
|---------|-----|-----------------|
| **Main API** | https://api.open-data.world | Docker Compose |
| **Lago Billing** | https://billing.open-data.world | Docker |
| **LangFlow** | https://flow.open-data.world | Docker |
| **n8n** | https://automate.open-data.world | Docker |
| **Flowise** | https://workflows.open-data.world | Docker |
| **Airflow** | https://airflow.open-data.world | Docker |
| **DataHub** | https://catalog.open-data.world | Docker |
| **OpenMetadata** | https://metadata.open-data.world | Docker |
| **Kafka** | https://stream.open-data.world | Docker |

## Quick Deploy Variables

```env
COMPOSE_PROJECT_NAME=data-platform
POSTGRES_PASSWORD=secure_password
POSTGRES_USER=admin
POSTGRES_DB=dataplatform
REDIS_PASSWORD=secure_password
OLLAMA_PORT=11434
LLM_MODEL=llama3
DOMAIN=open-data.world
```

## Coolify Resources Setup

### 1. Create PostgreSQL
- Type: PostgreSQL
- Version: 15
- Database: dataplatform
- Connection: `postgresql://admin:{password}@host:5432/dataplatform`

### 2. Create Redis
- Type: Redis
- Version: 7

### 3. Create Main Application (Docker Compose)
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: dataplatform

  redis:
    image: redis:7
    command: redis-server --requirepass ${REDIS_PASSWORD}

  orchestrator:
    build: ./orchestrator
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_URL=postgresql://admin:${POSTGRES_PASSWORD}@postgres:5432/dataplatform
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
```

## One-Click Deploy Script

For Coolify's "Custom Script" deploy option:

```bash
#!/bin/bash
set -e

echo "🚀 Deploying Data Platform to Coolify..."

# Clone repository if needed
# git clone https://github.com/yourorg/data-platform.git

cd /workspace/data-platform

# Set domain
export DOMAIN=open-data.world

# Start services
docker-compose --profile ingest up -d

echo "✅ Deployment complete!"
echo ""
echo "🌐 URLs:"
echo "  - API: https://api.${DOMAIN}"
echo "  - Billing: https://billing.${DOMAIN}"
echo "  - LangFlow: https://flow.${DOMAIN}"
```