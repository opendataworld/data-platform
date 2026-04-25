# Canonical Entity Directory

## Purpose

The Canonical Entity Directory is the governed source of truth for reusable entity identifiers across the data platform. It provides stable canonical IDs, trusted labels, aliases, external identifiers, lifecycle state, relationship metadata, audit history, and resolution APIs so datasets, schemas, vocabularies, taxonomies, pipelines, applications, and analytics products can refer to the same real-world entity consistently.

## Problem statement

Data producers frequently describe the same organization, dataset, location, person, concept, instrument, funder, publisher, or other domain object using different labels, spellings, local IDs, or source-system identifiers. This creates duplicate records, brittle joins, unclear lineage, unreliable reporting, and repeated manual reconciliation work.

The directory solves this by separating source-specific identifiers from platform-level canonical identifiers. It gives governance teams a controlled workflow for creating, reviewing, merging, deprecating, and retiring entity records while giving downstream systems a stable API for lookup and resolution.

## Product outcomes

- Every governed entity has one stable canonical ID.
- Source-system identifiers can be mapped to canonical IDs.
- Entity lifecycle status is explicit and visible to consumers.
- Duplicate entities are detected and remediated through merge workflows.
- Downstream references remain safe when entities are deprecated, retired, or merged.
- Entity changes are auditable and attributable.
- Consumers can resolve identifiers through reliable APIs and events.

## Product boundaries

### In scope

- Canonical entity creation and lifecycle management.
- Entity search and discovery.
- Alias and external identifier management.
- Entity relationship capture for lightweight graph-style references.
- Duplicate detection, merge, redirect, deprecation, and retirement workflows.
- Approval workflow for governed entity types.
- Read APIs, search APIs, and lifecycle event emission.
- Audit trail, permissions, and operational monitoring.

### Out of scope

- Full master data management with automated golden-record survivorship.
- Complex probabilistic entity-resolution pipelines as the primary source of truth.
- Rich knowledge-graph exploration UI.
- Domain-specific curation workflows that belong in downstream applications.
- Bulk data stewardship workbenches beyond import, validation, and review queues.

## Users and responsibilities

| Role | Responsibilities |
| --- | --- |
| Viewer | Search, inspect, and reference approved entities. |
| Contributor | Propose new entities and metadata changes. |
| Steward | Review, approve, reject, merge, deprecate, and retire entities. |
| Domain owner | Own quality, definitions, and lifecycle rules for specific entity types. |
| Platform engineer | Integrate resolution APIs, events, and downstream references. |
| Administrator | Configure entity types, required fields, permissions, retention, and integrations. |

## Entity lifecycle

| Status | Meaning | Allowed transitions |
| --- | --- | --- |
| `draft` | Entity exists as an unpublished proposal. | `in_review`, `retired` |
| `in_review` | Entity is waiting for steward decision. | `approved`, `draft`, `rejected` |
| `approved` | Entity is trusted for downstream use. | `deprecated`, `retired`, `merged` |
| `rejected` | Proposal was not accepted. | `draft` |
| `deprecated` | Entity should not be used for new references but remains valid for existing references. | `approved`, `retired`, `merged` |
| `retired` | Entity is no longer valid but remains resolvable for history. | None by default |
| `merged` | Entity was superseded by another canonical entity. | None by default |

Canonical IDs must never be reused, even after retirement or merge.

## Core workflows

### Create and approve entity

1. Contributor searches existing entities before creating a new one.
2. Contributor creates a draft with required metadata.
3. System validates required fields, identifier format, duplicate candidates, and policy rules.
4. Contributor submits entity for review.
5. Steward reviews metadata, duplicate warnings, source identifiers, and proposed ownership.
6. Steward approves, rejects, or requests changes.
7. Approved entity becomes searchable and available through APIs.

### Resolve external identifier

1. Consumer submits source name and source identifier.
2. Resolution service normalizes source and identifier values.
3. Service returns matching canonical entity, lifecycle status, version, and redirect target if applicable.
4. Consumer stores canonical ID rather than the source-specific ID when possible.

### Merge duplicates

1. Steward selects source entity and target entity.
2. System shows aliases, external IDs, relationships, downstream references, and conflicts.
3. Steward chooses conflict resolution rules.
4. System moves approved aliases and identifiers to the target entity.
5. Source entity becomes `merged` and redirects to target entity.
6. Merge event is emitted for downstream consumers.

### Deprecate or retire entity

1. Steward initiates lifecycle change with reason and optional replacement entity.
2. System shows downstream references and integration impact.
3. Steward confirms change.
4. Entity remains resolvable with status and replacement metadata.
5. Lifecycle event is emitted.

## Functional capabilities

### Entity records

- Create, view, edit, approve, reject, deprecate, retire, and merge entities.
- Support configurable entity types such as organization, person, place, dataset, publisher, funder, concept, and project.
- Capture canonical label, description, owner, domain, aliases, identifiers, relationships, lifecycle status, provenance, and version.
- Preserve immutable history of material changes.

### Search and discovery

- Search by canonical label, normalized label, alias, entity type, owner, domain, lifecycle status, and external identifier.
- Filter by created date, updated date, steward, and source system.
- Surface duplicate candidates during create and edit workflows.
- Show downstream references and replacement guidance.

### Governance

- Configurable required fields by entity type.
- Steward approval before an entity is marked approved.
- Mandatory notes for rejection, deprecation, retirement, and merge.
- Audit trail for all material changes.
- Role-based access controls for create, approve, merge, retire, and configure actions.

### Integration

- Read and search APIs for UI and downstream services.
- Identifier resolution API for ingestion pipelines.
- Lifecycle events for create, update, approve, merge, deprecate, and retire.
- Bulk import with validation and review queue.
- Export for backup, migration, and offline governance review.

## Data model

### Entity

```json
{
  "entity_id": "ent_org_01HZX7K9E2F3M4N5P6Q7R8S9T0",
  "entity_type": "organization",
  "canonical_label": "Example Research Institute",
  "normalized_label": "example research institute",
  "description": "Independent research organization focused on open data standards.",
  "status": "approved",
  "domain": "research-data",
  "owner": "data-governance",
  "version": 7,
  "created_at": "2026-04-25T00:00:00Z",
  "created_by": "user@example.org",
  "updated_at": "2026-04-25T00:00:00Z",
  "updated_by": "steward@example.org"
}
```

### Alias

```json
{
  "alias_id": "alias_01HZX8",
  "entity_id": "ent_org_01HZX7K9E2F3M4N5P6Q7R8S9T0",
  "label": "ERI",
  "normalized_label": "eri",
  "language": "en",
  "alias_type": "abbreviation",
  "status": "active"
}
```

### External identifier

```json
{
  "external_identifier_id": "xid_01HZX9",
  "entity_id": "ent_org_01HZX7K9E2F3M4N5P6Q7R8S9T0",
  "source": "ror",
  "identifier": "https://ror.org/000000000",
  "identifier_type": "registry_url",
  "confidence": "verified",
  "status": "active"
}
```

### Relationship

```json
{
  "relationship_id": "rel_01HZXA",
  "source_entity_id": "ent_org_01HZX7K9E2F3M4N5P6Q7R8S9T0",
  "relationship_type": "parent_of",
  "target_entity_id": "ent_org_01HZXB",
  "status": "active",
  "valid_from": "2026-04-25",
  "valid_to": null
}
```

### Redirect

```json
{
  "from_entity_id": "ent_org_old",
  "to_entity_id": "ent_org_new",
  "reason": "duplicate_merge",
  "created_at": "2026-04-25T00:00:00Z",
  "created_by": "steward@example.org"
}
```

## API surface

### Read APIs

- `GET /registries/entities/{entity_id}` returns entity detail, status, aliases, identifiers, relationships, version, and redirect target.
- `GET /registries/entities` searches entities with pagination and filters.
- `GET /registries/entities/resolve?source={source}&identifier={identifier}` resolves source identifiers to canonical IDs.
- `GET /registries/entities/{entity_id}/history` returns audit history.
- `GET /registries/entities/{entity_id}/references` returns known downstream references when available.

### Write APIs

- `POST /registries/entities` creates draft entity.
- `PATCH /registries/entities/{entity_id}` proposes or applies metadata changes according to permissions.
- `POST /registries/entities/{entity_id}/submit` submits draft for review.
- `POST /registries/entities/{entity_id}/approve` approves entity or change request.
- `POST /registries/entities/{entity_id}/reject` rejects entity or change request.
- `POST /registries/entities/{entity_id}/deprecate` deprecates approved entity.
- `POST /registries/entities/{entity_id}/retire` retires entity.
- `POST /registries/entities/merge` merges duplicate entities.

### Events

- `entity.created`
- `entity.updated`
- `entity.approved`
- `entity.rejected`
- `entity.deprecated`
- `entity.retired`
- `entity.merged`
- `entity.identifier.added`
- `entity.identifier.removed`

All events should include `event_id`, `event_type`, `entity_id`, `version`, `occurred_at`, `actor`, `correlation_id`, and payload diff where appropriate.

## Validation rules

- `entity_type` must be configured and active.
- `canonical_label` is required and must be unique within configured duplicate policy boundaries.
- `status` must be a valid lifecycle state.
- External identifier source must be configured before use.
- External identifier must be unique for a source unless explicitly configured as non-unique.
- Relationship targets must exist and must not create forbidden cycles where the relationship type is hierarchical.
- Merge source and target must be different entities.
- Retired or merged entities cannot become merge targets without administrator override.

## Permissions and access control

- Use role-based access control with optional domain scoping.
- Read access may be broad, but draft, rejected, and sensitive entity types can be restricted.
- Approval, merge, deprecation, retirement, and configuration changes require elevated roles.
- All privileged actions must be audit logged.
- Service accounts should use scoped tokens with least privilege.

## Security and privacy

- Treat person entities and any personally identifiable information as sensitive.
- Avoid storing unnecessary personal data in canonical records.
- Support redaction or restricted fields for sensitive entity types.
- Record actor identity for audit events.
- Protect write APIs with authentication, authorization, rate limiting, and input validation.
- Ensure exports respect permissions and privacy policies.

## Observability

Track these metrics:

- Entity count by type and status.
- Duplicate candidate rate.
- Merge rate and merge conflicts.
- Approval queue size and review latency.
- API latency, error rate, and lookup success rate.
- Identifier resolution miss rate by source.
- Event delivery success and retry count.
- Search indexing freshness.

Recommended alerts:

- Identifier resolution error rate exceeds threshold.
- Event delivery backlog exceeds threshold.
- Search index freshness exceeds SLA.
- Approval queue exceeds configured age or size.
- Merge operation fails after partial update attempt.

## Operational requirements

- Canonical IDs are immutable and never reused.
- Entity deletion is disallowed through normal product flows.
- Merge and lifecycle operations must be transactional or compensatable.
- Search index updates must be eventually consistent within a documented SLA.
- Audit log must be append-only from application perspective.
- Backups must include entity records, aliases, identifiers, relationships, redirects, and audit logs.
- Bulk imports must be resumable and produce validation reports.

## Failure modes

| Failure | Expected behavior |
| --- | --- |
| Search index unavailable | UI shows degraded search state and direct ID lookup remains available. |
| Duplicate detection unavailable | Creation can continue only if policy allows; warning is logged. |
| Merge conflict | Merge is blocked until steward resolves conflict. |
| Event delivery failure | Event is retried and visible in operational dashboard. |
| Downstream reference lookup failure | Retirement or merge warns steward before confirmation. |
| Partial import failure | Successful rows are recorded, failed rows include row-level errors, and job can resume. |

## Migration and adoption

1. Identify high-value entity types and source systems.
2. Define required fields, identifier sources, and steward ownership by type.
3. Import seed entities from trusted sources.
4. Run duplicate analysis before opening broad contribution.
5. Integrate identifier resolution into one ingestion pipeline.
6. Publish adoption guidance for analysts and engineers.
7. Expand to additional entity types and source identifiers after quality checks stabilize.

## Success metrics

- Percentage of governed datasets using canonical IDs.
- Reduction in duplicate entity records over time.
- Identifier resolution success rate by source.
- Median review time for proposed entities.
- Number of downstream systems consuming lifecycle events.
- Reduction in manual mapping spreadsheets or ad hoc lookup tables.

## Roadmap

### Foundation

- Entity types, lifecycle, search, approval, alias, external identifier, audit, read API, and resolution API.

### Scale

- Bulk import, duplicate review queue, downstream reference graph, event subscriptions, and richer data-quality dashboards.

### Intelligence

- Probabilistic duplicate suggestions, steward workload routing, source trust scoring, and automated enrichment from approved external registries.

## Open decisions

- Which entity types are production-critical for first launch?
- What canonical ID format should be standardized across registries?
- Which external identifier sources are required by entity type?
- What are the retention and privacy rules for person entities?
- Which downstream consumers require synchronous lookup versus event-based updates?
