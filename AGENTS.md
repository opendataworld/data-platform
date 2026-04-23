# AGENTS.md

## Repo Role

This repository is the umbrella repo for the **OpenDataWorld Data Platform**.

It is the main place for:
- deployment and integration
- local/dev platform assembly
- OSS service composition
- platform architecture documentation
- module and roadmap definition

It is **not** the AI Platform.
It is **not** the Identity Platform.
It is **not** the Intelligence Platform.

---

## Source of Truth Rules

### 1. Prompt Registry first
Before doing any work:

1. Save the current task prompt to the appropriate Prompt Registry location in GitHub
2. Read the stored prompt back from GitHub
3. Use the GitHub-stored version as the canonical prompt for execution

### 2. PRD first
Before making recommendations or changes:

1. Read the org-wide PRD from the Prompt Registry
2. Treat it as the architectural source of truth
3. Do not contradict it silently
4. If repo reality differs from the PRD, identify the mismatch explicitly and propose a correction

### 3. GitHub is the system of record
GitHub is the system of record for:
- prompts
- PRDs
- docs
- code
- outputs
- reviews
- approvals
- final published versions

Chat is for drafting.  
GitHub is for record, review, revision, approval, and publishing.

---

## Operating Rule

Build the product first.

If the repo structure, templates, docs, prompts, or this `AGENTS.md` file need improvement to support the product cleanly, update them in the same change set.

Do **not** redesign the whole platform before shipping the next usable product.

Make only the minimum structural changes needed for the current product, but leave the repo cleaner than you found it.

---

## Platform Context

- **OpenDataWorld** = Data Platform
- **AgentNxt** = AI Platform
- Data Platform is the current execution priority
- Every registry is the canonical system of record for its domain
- Canonicality is platform-wide
- We are not building one giant universal canonical bucket

### Long-term Data Platform direction
The Data Platform will support canonical records across domain registries such as:
- dataset registry
- schema registry
- taxonomy registry
- vocabulary registry
- entity registry
- thing registry
- publication registry
- license registry
- eval data registry

Do not force all of these into separate repos immediately.
Document the future structure first. Split only when boundaries are stable.

---

## OSS Strategy

Prefer:
1. integrate
2. compose
3. clone if helpful
4. fork only when durable product-specific customization is truly necessary

Do not rewrite mature OSS infrastructure unnecessarily.

Current important OSS foundations include:
- OpenMetadata
- Airbyte
- OpenLineage
- Marquez
- Zingg
- Cube
- Superset
- TerminusDB
- GraphDB
- Jena
- SurrealDB
- Postgres
- Redis
- Feast
- Label Studio
- Argilla
- SearXNG
- Firecrawl
- Crawl4AI
- Playwright

---

## Current Module Meanings

- **catalog** = metadata, discovery, asset visibility
- **lineage** = lineage standard + lineage backend
- **ingestion** = ETL, replication, crawl, acquisition
- **resolution** = canonicalization and entity resolution
- **semantic** = semantic metrics and modeling layer
- **visualization** = dashboards, charts, reports, graph/map/custom views
- **graph** = RDF, linked data, ontology, graph integrations
- **store** = operational and canonical storage backends
- **labeling** = human review, annotation, adjudication, feedback
- **features** = operational feature store layer
- **search** = internal and external search capability
- **docs** = architecture, setup, roadmap, and product-facing documentation

---

## What to Optimize For

Optimize for:
- practical progress
- clean architecture
- clear docs
- reviewable changes
- repo consistency
- explicit current vs next vs future state
- GitHub-backed prompt and output governance

Do not optimize for:
- abstract perfection
- premature repo splitting
- unnecessary rewrites
- undocumented architectural drift

---

## Required Execution Pattern

For each task:

1. Save prompt to Prompt Registry
2. Read prompt back from Prompt Registry
3. Read org PRD
4. Inspect current repo state
5. Build the requested product or capability slice
6. Update docs/structure only as needed
7. Save outputs in GitHub
8. Save review notes in GitHub
9. Keep final approved state in GitHub only

---

## Output Expectations

Every substantial task should clearly distinguish:
- **current state**
- **recommended next state**
- **future state**

Every substantial task should leave behind:
- updated files
- updated docs if needed
- clear review notes
- explicit follow-ups if unfinished

---

## If There Is a Conflict

If any of the following conflict:
- repo reality
- task prompt
- PRD
- existing docs

Then:
1. do not guess silently
2. state the conflict clearly
3. propose the smallest correction that moves the repo toward the PRD

---

## Default Priority

When in doubt, prioritize:
1. shipping a usable product slice
2. clarifying repo structure
3. improving docs and prompts
4. preparing future modularization
