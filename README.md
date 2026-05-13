# Open Source Data Management Solutions

A comprehensive list of Apache 2.0 and MIT licensed open source solutions for data management, aligned with the [IBM Data Management Guide](https://www.ibm.com/think/topics/data-management-guide).

## Table of Contents

1. [Database Management](#1-database-management)
2. [Data Warehouse & Lakehouse](#2-data-warehouse--lakehouse)
3. [Data Integration & ETL](#3-data-integration--etl)
4. [Data Governance](#4-data-governance)
5. [Master Data Management](#5-master-data-management)
6. [Stream Processing](#6-stream-processing)
7. [Business Intelligence & Visualization](#7-business-intelligence--visualization)
8. [ML/AI & Feature Store](#8-mlai--feature-store)
9. [Data Observability](#9-data-observability)

---

## 1. Database Management

### Relational Databases

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| PostgreSQL | PostgreSQL | Open-source relational database with extensibility | https://www.postgresql.org/ |
| MySQL | GPL v2 | Popular open-source relational database | https://www.mysql.com/ |
| MariaDB | GPL v2 | MySQL fork with additional features | https://mariadb.org/ |
| SQLite | Public Domain | In-process database engine | https://www.sqlite.org/ |

### Distributed NoSQL

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Cassandra | Apache 2.0 | Distributed NoSQL database, scalable with high availability | https://cassandra.apache.org/ |
| Apache HBase | Apache 2.0 | Wide-column store for Hadoop | https://hbase.apache.org/ |
| Apache CouchDB | Apache 2.0 | Document-oriented database | https://couchdb.apache.org/ |
| Couchbase | Apache 2.0 | Distributed NoSQL database | https://www.couchbase.com/ |
| MongoDB | SSPL | Document-oriented database | https://www.mongodb.com/ |
| Redis | BSD | In-memory data structure store | https://redis.io/ |
| Valkey | BSD 3-Clause | Redis fork | https://valkey.io/ |

### NewSQL

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| TiDB | Apache 2.0 | Distributed SQL database | https://pingcap.com/ |
| CockroachDB | MIT/BSL | Distributed SQL for global apps | https://www.cockroachlabs.com/ |
| YugabyteDB | Apache 2.0 | Distributed SQL database | https://www.yugabyte.com/ |

### Time-Series Databases

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| TimescaleDB | Apache 2.0 | Time-series database built on PostgreSQL | https://www.timescale.com/ |
| InfluxDB | MIT | Time-series database | https://www.influxdata.com/ |
| QuestDB | Apache 2.0 | Time-series SQL database | https://questdb.io/ |
| Apache Druid | Apache 2.0 | Column-oriented distributed data store | https://druid.apache.org/ |

### Graph Databases

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Neo4j | GPL (Community) | Graph database | https://neo4j.com/ |
| Apache Jena | Apache 2.0 | RDF framework | https://jena.apache.org/ |

### Vector Databases (AI/ML)

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Milvus | Apache 2.0 | Open-source vector database | https://milvus.io/ |
| Qdrant | Apache 2.0 | Vector similarity search engine | https://qdrant.tech/ |
| Weaviate | BSD-3-Clause | Cloud-native vector database | https://weaviate.io/ |
| Chroma | Apache 2.0 | AI-native vector database | https://www.trychroma.com/ |
| Faiss | MIT | Facebook AI Similarity Search | https://github.com/facebookresearch/faiss |
| pgvector | PostgreSQL | Vector similarity search for PostgreSQL | https://github.com/pgvector/pgvector |
| OpenSearch | Apache 2.0 | Distributed search and analytics engine | https://opensearch.org/ |
| Vespa | Apache 2.0 | Vector search engine | https://vespa.ai/ |

---

## 2. Data Warehouse & Lakehouse

### Table Formats (Lakehouse)

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Iceberg | Apache 2.0 | Open table format for petabyte-scale | https://iceberg.apache.org/ |
| Delta Lake | Apache 2.0 | ACID transactions on storage | https://delta.io/ |
| Apache Hudi | Apache 2.0 | Incremental processing | https://hudi.apache.org/ |

### Data Warehouses

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Doris | Apache 2.0 | Real-time analytics database | https://doris.apache.org/ |
| ClickHouse | Apache 2.0 | Column-oriented OLAP database | https://clickhouse.com/ |
| Greenplum | Apache 2.0 | MPP analytics platform | https://greenplum.org/ |

### Query Engines

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Spark | Apache 2.0 | Unified analytics engine | https://spark.apache.org/ |
| Trino | Apache 2.0 | Distributed SQL query engine | https://trino.io/ |
| Presto | Apache 2.0 | SQL query for big data | https://prestodb.io/ |
| Apache Flink | Apache 2.0 | Stream processing engine | https://flink.apache.org/ |
| Apache Beam | Apache 2.0 | Unified programming model | https://beam.apache.org/ |

---

## 3. Data Integration & ETL

### Orchestration & Scheduling

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Airflow | Apache 2.0 | Workflow platform | https://airflow.apache.org/ |
| Dagster | Apache 2.0 | Modern data orchestrator | https://dagster.io/ |
| Prefect | Apache 2.0 | Workflow management | https://www.prefect.io/ |
| Luigi | Apache 2.0 | Python pipeline orchestration | https://luigi.readthedocs.io/ |
| Apache NiFi | Apache 2.0 | Dataflow automation | https://nifi.apache.org/ |
| Argo Workflows | Apache 2.0 | Container-native workflow engine | https://argoproj.github.io/ |
| Kafka Connect | Apache 2.0 | Streaming integration | https://kafka.apache.org/ |
| Kestra | Apache 2.0 | Event-driven orchestrator | https://kestra.io/ |

### Data Processing

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| dbt | Apache 2.0 | Transform in warehouse using SQL | https://www.getdbt.com/ |
| Apache Beam | Apache 2.0 | Unified batch/streaming | https://beam.apache.org/ |
| Pandas | BSD-3-Clause | Data manipulation | https://pandas.pydata.org/ |
| PySpark | Apache 2.0 | Python API for Spark | https://spark.apache.org/ |
| Dask | BSD-3-Clause | Parallel computing | https://www.dask.org/ |

### CDC (Change Data Capture)

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Debezium | Apache 2.0 | CDC platform | https://debezium.io/ |
| Airbyte | MIT | ELT platform | https://airbyte.com/ |
| Singer | Apache 2.0 | ETL standard | https://www.singer.io/ |

---

## 4. Data Governance

### Metadata Management & Data Catalog

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Atlas | Apache 2.0 | Metadata & governance | https://atlas.apache.org/ |
| DataHub | Apache 2.0 | Metadata platform (LinkedIn) | https://datahubproject.io/ |
| OpenMetadata | Apache 2.0 | Unified metadata | https://open-metadata.org/ |
| Amundsen | Apache 2.0 | Data discovery (Lyft) | https://www.amundsen.io/ |
| Marquez | Apache 2.0 | OpenLineage backend | https://marquezproject.github.io/ |
| Metacat | Apache 2.0 | Metadata (Netflix) | https://github.com/Netflix/metacat |
| OpenDataDiscovery | Apache 2.0 | Data observability | https://opendatadiscovery.org/ |
| Egeria | Apache 2.0 | Open metadata | https://odpi.github.io/ |

### Data Lineage

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| OpenLineage | Apache 2.0 | Lineage standard & collection | https://openlineage.io/ |
| Marquez | Apache 2.0 | Lineage metadata repository | https://marquezproject.github.io/ |
| Spline | Apache 2.0 | Data lineage tracking | https://github.com/AbsaOSS/Spline |
| Grai | MIT | Data lineage tool | https://grai.io/ |
| LakeFS | Apache 2.0 | Data version control | https://lakefs.io/ |

### Data Quality

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Great Expectations | Apache 2.0 | Data validation platform | https://greatexpectations.io/ |
| Deequ | Apache 2.0 | Unit tests for data (Spark) | https://github.com/awslabs/deequ |
| Soda Core | Apache 2.0 | Data quality checks | https://github.com/sodadata/soda-core |
| Elementary | MIT | dbt native monitoring | https://github.com/elementary-data/elementary |
| dbt-expectations | MIT | dbt custom expectations | https://github.com/calogica/dbt-expectations |

### Security & Access Control

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Ranger | Apache 2.0 | Security for Hadoop | https://ranger.apache.org/ |
| Apache Sentry | Apache 2.0 | Authorization | https://sentry.apache.org/ |

---

## 5. Master Data Management

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Fuyuko | Apache 2.0 | MDM/PIM | https://github.com/tmjeee/fuyuko |

---

## 6. Stream Processing

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Kafka | Apache 2.0 | Distributed event streaming | https://kafka.apache.org/ |
| Apache Flink | Apache 2.0 | Stream processing | https://flink.apache.org/ |
| Apache Pulsar | Apache 2.0 | Messaging and streaming | https://pulsar.apache.org/ |
| StreamSets | Apache 2.0 | Data collector | https://streamsets.com/ |
| Redpanda | Apache 2.0 | Kafka-compatible | https://redpanda.com/ |
| Apache Storm | Apache 2.0 | Real-time computation | https://storm.apache.org/ |

---

## 7. Business Intelligence & Visualization

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Apache Superset | Apache 2.0 | Data visualization | https://superset.apache.org/ |
| Metabase | AGPL | Simple BI tool | https://www.metabase.com/ |
| Redash | BSD | Query & visualization | https://redash.io/ |
| Grafana | AGPL | Observability dashboards | https://grafana.com/ |
| KNOWAGE | Apache 2.0 | Analytics platform | https://www.knowage-suite.eu/ |
| Jaspersoft | GPL | Reporting | https://community.jaspersoft.com/ |
| Evidence | MIT | SQL-based BI | https://evidence.dev/ |
| Lightdash | MIT | dbt-integrated BI | https://lightdash.io/ |

---

## 8. ML/AI & Feature Store

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| MLflow | Apache 2.0 | ML lifecycle | https://mlflow.org/ |
| Feast | Apache 2.0 | Feature store | https://feast.dev/ |
| TensorFlow | Apache 2.0 | Deep learning | https://www.tensorflow.org/ |
| PyTorch | BSD | Deep learning | https://pytorch.org/ |
| Kubeflow | Apache 2.0 | ML toolkit for K8s | https://kubeflow.org/ |
| CML | Apache 2.0 | Continuous ML | https://cml.dev/ |

---

## 9. Data Observability

| Tool | License | Description | Source |
|------|---------|-------------|--------|
| Prometheus | Apache 2.0 | Monitoring | https://prometheus.io/ |
| OpenTelemetry | Apache 2.0 | Collection | https://opentelemetry.io/ |
| Grafana | AGPL | Visualization | https://grafana.com/ |

---

## License Summary

| License | Tools Count |
|---------|----------|
| Apache 2.0 | 60+ |
| MIT | 8 |
| BSD | 5 |
| AGPL | 2 |
| PostgreSQL | 1 |
| GPL | 2 |

---

## Contributing

To contribute to this list:
1. Fork the repository
2. Add the tool with license and source
3. Submit a PR

---

## References

- [IBM Data Management Guide](https://www.ibm.com/think/topics/data-management-guide)
- [Apache Software Foundation](https://www.apache.org/)
- [Open Source Initiative](https://opensource.org/)