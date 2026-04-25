# Canonical Entity Directory MVP

## Status

- **Product area:** Registries
- **Lifecycle stage:** MVP definition
- **Primary users:** Data stewards, data engineers, analysts, API consumers, governance administrators
- **Primary outcome:** Provide a trusted directory of canonical entities and stable identifiers that downstream datasets, vocabularies, taxonomies, and schemas can reference consistently.

## Problem statement

Teams need a reliable way to identify and reuse the same real-world entity across datasets. Without a canonical directory, the same organization, place, concept, product, person, or dataset object can appear under different labels, IDs, spellings, or source-specific keys. This creates duplicate records, inconsistent joins, unclear lineage, and avoidable manual reconciliation.

The MVP creates a governed directory where approved canonical entities can be created, searched, linked to external identifiers, versioned, and retired without breaking downstream references.

## Goals

- Establish stable canonical identifiers for governed entities.
- Make entities searchable by label, alias, type, external ID, and status.
- Capture the minimum metadata required for trust, lineage, and reuse.
- Support steward review before an entity becomes approved.
- Provide API-ready entity records for downstream platform services.
- Maintain a clear audit trail for creates, edits, merges, deprecations, and retirements.

## Non-goals

- Full master-data-management workflows such as survivorship rules, automated golden-record creation, or complex householding.
- Bulk entity-resolution machine learning.
- Real-time synchronization with every external source system.
- Advanced graph exploration or entity relationship visualization.
- Custom entity-type modeling beyond a small governed set of MVP entity types.

## MVP users and jobs

| User | Job to be done |
| --- | --- |
| Data steward | Create, review, approve, merge, and retire canonical entities. |
| Data engineer | Resolve source-specific identifiers to canonical IDs during ingestion. |
| Analyst | Search for the right entity before building a dataset, dashboard, or report. |
| API consumer | Retrieve canonical entity metadata and status through a stable API contract. |
| Governance administrator | Configure allowed entity types, required fields, and approval permissions. |

## MVP scope

### Entity management

- Create an entity with required metadata.
- Edit draft or approved entity metadata with audit history.
- Assign entity type from an approved controlled list.
- Set lifecycle status: `draft`, `in_review`, `approved`, `deprecated`, `retired`.
- Add aliases and source-system identifiers.
- Merge duplicate entities while preserving redirect metadata from retired IDs.
- Retire an entity with required reason and replacement reference when available.

### Search and discovery

- Search by canonical label, alias, entity type, external identifier, status, and owner.
- Show entity detail page with metadata, aliases, external IDs, relationships, status, history, and downstream references.
- Flag duplicate candidates using exact and normalized label matching.

### Governance workflow

- Require steward approval before an entity becomes `approved`.
- Capture reviewer, timestamp, change summary, and decision notes.
- Restrict destructive actions such as merge and retirement to authorized roles.

### API and integration

- Provide read endpoints for entity lookup by canonical ID and external ID.
- Provide list/search endpoints with pagination and filters.
- Emit structured events for create, update, approval, merge, deprecation, and retirement.
- Expose version and status fields so consumers can handle changes safely.

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| CED-001 | Users can create draft canonical entities with required fields. | Must |
| CED-002 | Users can search entities by label, alias, external ID, type, and status. | Must |
| CED-003 | Approved entities receive stable canonical IDs that are never reused. | Must |
| CED-004 | Users can add multiple aliases and source identifiers to an entity. | Must |
| CED-005 | Stewards can approve, reject, deprecate, retire, and merge entities. | Must |
| CED-006 | The system records an immutable audit trail for material changes. | Must |
| CED-007 | Consumers can resolve external IDs to canonical IDs through an API. | Must |
| CED-008 | Duplicate candidates are highlighted during create and edit flows. | Should |
| CED-009 | Downstream references are shown before retirement or merge. | Should |
| CED-010 | Entity records can be exported as JSON for platform integrations. | Could |

## Minimum data model

```json
{
  "entity_id": "ent_org_01HZX7K9E2F3M4N5P6Q7R8S9T0",
  "entity_type": "organization",
  "canonical_label": "Example Research Institute",
  "description": "Independent research organization focused on open data standards.",
  "status": "approved",
  "aliases": [
    "ERI",
    "Example Research Inst."
  ],
  "external_identifiers": [
    {
      "source": "ror",
      "identifier": "https://ror.org/000000000"
    }
  ],
  "relationships": [
    {
      "relationship_type": "parent_of",
      "target_entity_id": "ent_org_01HZX8..."
    }
  ],
  "owner": "data-governance",
  "created_at": "2026-04-25T00:00:00Z",
  "created_by": "user@example.org",
  "updated_at": "2026-04-25T00:00:00Z",
  "updated_by": "user@example.org",
  "version": 1
}
```

## Permissions

| Role | Capabilities |
| --- | --- |
| Viewer | Search and view approved entities. |
| Contributor | Create drafts and propose changes. |
| Steward | Approve, reject, deprecate, retire, and merge entities. |
| Administrator | Configure entity types, required fields, and role mappings. |

## Workflow

1. Contributor searches for an existing entity.
2. If no suitable entity exists, contributor creates a draft entity.
3. System validates required metadata and flags likely duplicates.
4. Contributor submits the draft for review.
5. Steward approves, rejects, or requests changes.
6. Approved entity becomes available through UI search and API lookup.
7. Later changes create a new version and audit event.
8. Merge or retirement requires steward action and preserves redirect metadata.

## Acceptance criteria

- A user can create, submit, approve, search, and retrieve a canonical entity from the UI and API.
- Canonical IDs are stable, unique, and never reused after retirement.
- Entity status is visible in UI and API responses.
- Duplicate warning appears when a new entity label matches an existing canonical label or alias after normalization.
- Every create, approve, edit, merge, deprecate, and retire action is audit logged.
- Unauthorized users cannot approve, merge, or retire entities.

## Success metrics

- At least 90% of new governed datasets reference approved canonical IDs where required.
- Duplicate entity creation rate falls month over month after launch.
- Median steward review time is less than two business days.
- API lookup success rate is at least 99.5% for valid canonical IDs.
- Fewer ad hoc identifier-mapping spreadsheets are created by data teams.

## Operational requirements

- All API responses include version, status, created timestamp, and updated timestamp.
- Entity deletion is not allowed in the MVP; retirement is used instead.
- Merge operations must preserve source entity IDs as redirects.
- Audit logs must be retained according to platform governance policy.
- Search index updates must complete within a documented freshness window.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Users create duplicates before searching. | Place search and duplicate warning in the create flow. |
| Downstream consumers depend on retired IDs. | Preserve redirects and expose replacement entity references. |
| Entity type scope expands too quickly. | Limit MVP to governed entity types approved by administrators. |
| Stewards become approval bottlenecks. | Track review SLAs and allow delegation by entity type. |

## Rollout plan

1. Seed a small set of high-value entity types and sample records.
2. Launch with data-governance administrators and a pilot data-engineering team.
3. Validate API lookup integration with one ingestion pipeline.
4. Open read-only discovery to analysts.
5. Expand contributor access after duplicate and review workflows are stable.

## Open questions

- Which entity types are in the first production release?
- What ID format should become the platform standard?
- Which external identifier systems are mandatory by entity type?
- What freshness SLA is required for search and API reads?
- Which downstream systems must receive entity lifecycle events first?
