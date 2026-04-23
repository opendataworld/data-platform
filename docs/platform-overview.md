# OpenDataWorld Data Platform Overview

## Purpose

`opendataworld/data-platform` is the umbrella integration repo for the OpenDataWorld Data Platform. It combines deployable OSS services, environment composition, and platform documentation in one reviewable place.

## Scope boundaries

### In scope
- Data platform composition and deployment
- Metadata/catalog, ingestion, lineage, storage, semantic modeling, visualization, graph, search, and labeling foundations
- Docs that define current architecture and staged evolution

### Out of scope
- AgentNxt AI Platform product scope
- Identity platform ownership (for example, external Keycloak lifecycle)
- Rewriting mature upstream systems already suited to the platform

## Current state

The repository currently acts as an umbrella Compose-based deployment workspace with broad profile coverage and multiple OSS dependencies already wired at varying maturity levels.

## Recommended next state

- Keep this repo as the main umbrella integration surface.
- Clarify module intent and boundaries in docs (without immediate repo sprawl).
- Improve reliability of profile documentation so docs match actual compose configuration.
- Add/strengthen lineage and feature-store pathways (for example Marquez, Feast) where useful.

## Future state (modular split, when stable)

Future modularization may split specific domains (for example registry-heavy domains or productized services) into dedicated repos once boundaries are operationally stable, governance is clear, and maintenance burden justifies separation.

Until then, this umbrella repo remains the canonical execution surface for integration.
