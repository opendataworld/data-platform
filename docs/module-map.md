# Data Platform Module Map

This document defines module meanings and distinguishes between current deployment reality and future architecture intent.

## Module definitions

- **catalog**: metadata, discovery, governance, and asset visibility.
- **lineage**: lineage standards, lineage collection, and lineage backend services.
- **ingestion**: ETL/ELT, replication, crawling, and acquisition workflows.
- **resolution**: canonicalization and entity resolution workflows.
- **semantic**: semantic modeling and metrics serving.
- **visualization**: dashboards, charts, reports, graph/map/custom views.
- **graph**: RDF, linked data, ontology, triple-store and graph integrations.
- **store**: operational and canonical storage backends.
- **labeling**: human annotation, adjudication, and feedback loops.
- **features**: operational feature-store and feature serving layer.
- **search**: internal and external search and retrieval capability.
- **docs**: architecture, setup, roadmap, and product-facing documentation.
- **registries** (future): canonical domain registries (dataset, schema, taxonomy, vocabulary, entity, thing, publication, license, eval data).

## Current state mapping (repo today)

- Implemented primarily through Docker Compose profiles and related docs.
- Several module concerns are represented directly as profiles (for example `catalog`, `ingest`, `resolve`, `semantic`, `viz`, `store`, `search`, `label`).
- Some module names in this architecture map do not yet appear one-to-one as profile names (for example `lineage`, `features`, `registries`) and should be treated as platform-level capabilities rather than immediate profile contracts.

## Recommended next state

- Keep module definitions stable in docs as product language.
- Incrementally align profile names, docs, and service bundles to reduce ambiguity.
- Introduce explicit lineage and feature-store service paths where they provide practical value.

## Future modular split guidance

Potential future split should be staged and evidence-based:
1. Keep umbrella repo as integration control plane.
2. Split only high-change/high-ownership modules after boundaries are proven.
3. Keep registry domains documented first, then split if and when operations demand it.
