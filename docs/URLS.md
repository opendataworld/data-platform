# Data Platform URLs - open-data.world with Coolify

## Production URLs

| Service | URL | Coolify Resource |
|---------|-----|-----------------|
| **Main API** | https://api.open-data.world | Docker Compose |
| **API Docs** | https://api.open-data.world/docs | - |
| **Lago Billing** | https://billing.open-data.world | Docker |
| **LangFlow** | https://flow.open-data.world | Docker |
| **n8n** | https://automate.open-data.world | Docker |
| **Flowise** | https://workflows.open-data.world | Docker |
| **Airflow** | https://airflow.open-data.world | Docker |
| **Prefect** | https://prefect.open-data.world | Docker |
| **Dagster** | https://dagster.open-data.world | Docker |
| **DataHub** | https://catalog.open-data.world | Docker |
| **Atlas** | https://atlas.open-data.world | Docker |
| **OpenMetadata** | https://metadata.open-data.world | Docker |
| **Marquez** | https://lineage.open-data.world | Docker |
| **Kafka** | https://stream.open-data.world | Docker |
| **Trino** | https://query.open-data.world | Docker |
| **Apache Pinot** | https://analytics.open-data.world | Docker |
| **ClickHouse** | https://warehouse.open-data.world | Docker |

## Coolify Management

| Service | URL |
|---------|-----|
| Coolify UI | https://coolify.open-data.world |

## Internal Services (No External URL)

| Service | Internal Port |
|---------|--------------|
| PostgreSQL | 5432 |
| Redis | 6379 |
| Ollama | 11434 |

## Deployment with Coolify

### Quick Start
```bash
# Copy environment file
cp .env.coolify .env

# Start services
docker-compose --profile ingest up -d
```

### Traefik (Automatic HTTPS)
All external URLs are configured with Traefik labels for automatic SSL via Let's Encrypt.