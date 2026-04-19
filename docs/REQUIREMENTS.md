# Data Platform - Disk Space Requirements

## Minimum Requirements

### Core Services Only (Startup)
| Service | Disk Space |
|---------|------------|
| PostgreSQL | 5 GB |
| Redis | 500 MB |
| Orchestrator | 1 GB |
| LangFlow | 2 GB |
| Lago | 1 GB |
| Traefik | 100 MB |
| **Total** | **~10 GB** |

### On-Demand Services (Deploy when needed)

| Service | Disk Space | Trigger |
|---------|------------|---------|
| Ollama (7B) | 4 GB | Agent request |
| Sentence-Transformers | 400 MB | Agent request |
| BGE Embeddings | 400 MB | Agent request |
| n8n | 3 GB | Agent request |
| Airflow | 5 GB | Agent request |
| DataHub | 10 GB | Agent request |
| ClickHouse | 20 GB | Agent request |
| Kafka | 5 GB | Agent request |
| Trino | 5 GB | Agent request |

### Full Platform (All Services)
| Service | Disk Space |
|---------|------------|
| Core | 10 GB |
| ML/AI Models | 30 GB |
| Data Stores | 50 GB |
| Workflows | 15 GB |
| Governance | 20 GB |
| **Total** | **~125 GB** |

## Recommended Storage

### Production (Core + On-Demand)
- **SSD**: 100 GB minimum
- **HDD**: 250 GB recommended

### Production (Full Platform)
- **SSD**: 250 GB minimum
- **HDD**: 500 GB+ recommended