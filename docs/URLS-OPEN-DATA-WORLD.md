# Data Platform URLs - open-data.world

## Production URLs

| Service | URL | Description |
|--------|-----|-------------|
| **Main API** | https://api.open-data.world | Unified API server |
| **API Docs** | https://api.open-data.world/docs | Swagger docs |

## Orchestrator

| Service | URL |
|---------|-----|
| Orchestrator | https://api.open-data.world |
| MCP Server | https://api.open-data.world/mcp |

## Billing (Lago)

| Service | URL |
|---------|-----|
| Lago UI | https://billing.open-data.world |
| Lago API | https://billing.open-data.world/api/v1 |

## Workflow / Low-Code

| Service | URL |
|---------|-----|
| LangFlow | https://flow.open-data.world |
| n8n | https://automate.open-data.world |
| Flowise | https://workflows.open-data.world |
| Chainlit | https://api.open-data.world/chainlit |

## Workflow Engines

| Service | URL |
|---------|-----|
| Airflow | https://airflow.open-data.world |
| Prefect | https://prefect.open-data.world |
| Dagster | https://dagster.open-data.world |

## Data Quality

| Service | URL |
|---------|-----|
| Great Expectations | https://api.open-data.world/great-expectations |
| Soda Core | https://api.open-data.world/soda |

## Data Governance

| Service | URL |
|---------|-----|
| DataHub | https://catalog.open-data.world |
| Atlas | https://atlas.open-data.world |
| OpenMetadata | https://metadata.open-data.world |
| Marquez | https://lineage.open-data.world |

## Streaming

| Service | URL |
|---------|-----|
| Kafka | https://stream.open-data.world |

## Data Integration

| Service | URL |
|---------|-----|
| Trino | https://query.open-data.world |
| Apache Pinot | https://analytics.open-data.world |
| ClickHouse | https://warehouse.open-data.world |

## Database (Internal)

| Service | Port |
|---------|------|
| PostgreSQL | 5432 |
| Redis | 6379 |
| SurrealDB | 8000 |

## Deployment

```bash
# Use production config
cp docker-compose.open-data.world.yml docker-compose.override.yml

# Set environment
export POSTGRES_PASSWORD=secure_password
export REDIS_PASSWORD=secure_password

# Start services
docker-compose --profile ingest up -d
```

## Traefik Configuration

All services are configured with Traefik labels for automatic HTTPS via Let's Encrypt.

### Certificate
- Provider: Let's Encrypt (automatic)
- HTTPS: Enabled on all external URLs