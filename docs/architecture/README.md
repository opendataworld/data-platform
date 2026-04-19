# Data Platform Architecture

## Overview

The Data Platform is an enterprise-grade data management system with 60+ integrated services, aligned with the IBM Data Management Guide and powered by AutonomyX agent specification.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Clients                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │LangFlow │  │ MCP    │  │REST API │  │Agents  │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  │
└───────┼──────────┼──────────┼──────────┼──────────┼──────────┘
        │          │          │          │
        ▼          ▼          ▼          ▼
┌──────────────────────────────────────────────────────────────┐
│                Orchestrator Agent                         │
│  ┌──────────────────────────────────────────────┐   │
│  │  LangGraph + AutonomyX + Billing         │   │
│  └──────────────────────────────────────────────┘   │
│        │          │          │          │             │
│        ▼          ▼          ▼          ▼             │
│   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
│   │Tools   │ │Service │ │Billing │ │Agent   │  │
│   │Registry│ │Registry│ │Tracker │ │Registry│  │
│   └────────┘ └────────┘ └────────┘ └────────┘  │
└───────────────────────────────────────────────┬──────┘
                                               │
        ┌───────────────┬───────────────┬──────────────┬────────────┐
        ▼           ▼           ▼            ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐
   │Crawling│ │Embedding│ │LLM      │ │Data     │ │Billing  │
   │Services│ │Services │ │Services │ │Quality  │ │Lago    │
   └─────────┘ └─────────┘ └─────────┘ └──────────┘ └──────────┘
```

## Service Categories (IBM Guide Aligned)

| Category | Services |
|----------|----------|
| Data Platforms | Postgres, ClickHouse, Trino, DuckDB |
| Data Architecture | DataHub, Atlas, Collibra, OpenMetadata |
| Data Engineering | Airflow, Dagster, Prefect, Temporal |
| Data Transfer | rclone, Airbyte, Meltano, Debezium |
| Data Integration | Trino, Apache Pinot |
| Data Quality | Great Expectations, Soda Core |
| Data Governance | Marquez, DataHub |
| Data SLA | Prometheus |

## ML/AI Pipeline

```
Crawl → Extract → Chunk → Embed → Store → Query → LLM
              ↓                               ↓
         OCR/NER                    Response
```

## AutonomyX Agent Flow

```
User Input → Agent Node → Tool Selection → Tool Execution → Response
                  ↓
            AutonomyX Audit
                  ↓
            Lago Billing
```

## Data Flow

1. **Ingestion**: Crawl websites, ingest files
2. **Processing**: OCR, chunking, embeddings
3. **Storage**: Vector DB, relational DB
4. **Query**: LLM, semantic search
5. **Governance**: Lineage, quality, catalog
6. **Billing**: Usage tracking

## Scalability

- Horizontal scaling via Docker Compose profiles
- Service-specific resource allocation
- Queue-based async processing
- Caching layer for embeddings