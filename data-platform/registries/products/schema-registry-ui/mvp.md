# Schema Registry UI MVP

## Status

- **Product area:** Registries
- **Lifecycle stage:** MVP definition
- **Primary users:** Data producers, data consumers, data stewards, platform engineers, governance administrators
- **Primary outcome:** Provide a governed user interface for discovering, reviewing, validating, and managing data schemas across the platform.

## Problem statement

Schemas are often managed as files, tickets, or tribal knowledge. This makes it difficult for teams to understand which schemas exist, which version is approved, what changed between versions, and whether a dataset conforms to the expected contract. The MVP creates a production-grade registry UI that makes schemas discoverable, reviewable, and operationally trustworthy.

## Goals

- Make approved and draft schemas easy to discover and compare.
- Support schema version review and lifecycle governance.
- Allow users to validate schema definitions before approval.
- Show ownership, compatibility status, and downstream usage signals.
- Provide a clear interface for managing schema metadata and status.

## Non-goals

- Replacing the underlying schema storage or validation engine.
- Building a full data catalog.
- Supporting every schema language in the first release.
- Visual schema modeling or drag-and-drop schema design.
- Automated semantic compatibility decisions beyond configured validation rules.

## MVP users and jobs

| User | Job to be done |
| --- | --- |
| Data producer | Submit and update schemas for datasets, events, or APIs. |
| Data consumer | Find the current approved schema and understand recent changes. |
| Data steward | Review schema metadata, approve versions, and enforce governance. |
| Platform engineer | Validate compatibility and troubleshoot contract failures. |
| Governance administrator | Configure required metadata, allowed schema types, and approval rules. |

## MVP scope

### Schema discovery

- List schemas with search, filters, owner, status, schema type, and updated date.
- View schema detail page with current version, status, owner, description, fields, validation results, and change history.
- Compare two schema versions using a readable diff.

### Schema lifecycle

- Create a draft schema entry.
- Upload or paste schema content.
- Validate syntax and required metadata before submission.
- Submit a schema version for review.
- Approve, reject, deprecate, or retire a schema version.
- Preserve immutable version history.

### Validation and compatibility

- Validate schema syntax for supported schema types.
- Run compatibility checks against the previous approved version when available.
- Show validation errors with actionable messages.
- Store validation results with timestamp and validator version.

### Governance metadata

- Capture owner, domain, description, schema type, compatibility mode, lifecycle status, tags, and related dataset or API references.
- Require approval notes for rejection, deprecation, and retirement.
- Show audit history for material changes.

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| SRU-001 | Users can search and filter schema records. | Must |
| SRU-002 | Users can view schema metadata, fields, versions, and status. | Must |
| SRU-003 | Contributors can create draft schema versions. | Must |
| SRU-004 | The UI validates schema syntax before submission. | Must |
| SRU-005 | The UI shows compatibility results against the latest approved version. | Must |
| SRU-006 | Stewards can approve, reject, deprecate, and retire schema versions. | Must |
| SRU-007 | Users can compare two schema versions. | Should |
| SRU-008 | Audit history is visible to authorized users. | Should |
| SRU-009 | Schema records can link to datasets, APIs, or events. | Should |
| SRU-010 | Users can copy a schema version as JSON. | Could |

## Supported schema types for MVP

The MVP should begin with a deliberately small supported set. Recommended first release:

- JSON Schema
- Avro Schema

Additional formats such as Protobuf, OpenAPI, and SQL DDL can be added after the validation and lifecycle workflow is stable.

## Minimum data model

```json
{
  "schema_id": "sch_01HZX7K9E2F3M4N5P6Q7R8S9T0",
  "name": "research_dataset_record",
  "display_name": "Research Dataset Record",
  "description": "Schema for dataset metadata records submitted to the platform.",
  "schema_type": "json_schema",
  "domain": "research-data",
  "owner": "data-platform",
  "status": "approved",
  "compatibility_mode": "backward",
  "current_version": "1.0.0",
  "tags": ["datasets", "metadata"],
  "versions": [
    {
      "version": "1.0.0",
      "status": "approved",
      "content_hash": "sha256:...",
      "validation_status": "passed",
      "compatibility_status": "passed",
      "created_at": "2026-04-25T00:00:00Z",
      "created_by": "user@example.org"
    }
  ]
}
```

## Permissions

| Role | Capabilities |
| --- | --- |
| Viewer | Search, view, compare, and copy approved schemas. |
| Contributor | Create drafts and submit schema versions for review. |
| Steward | Approve, reject, deprecate, and retire schema versions. |
| Administrator | Configure schema types, metadata rules, compatibility modes, and role mappings. |

## Workflow

1. Contributor searches for an existing schema.
2. Contributor creates a draft schema or new version.
3. UI validates syntax and required metadata.
4. Contributor submits the version for review.
5. System runs compatibility checks against the latest approved version.
6. Steward reviews metadata, diff, validation results, and compatibility results.
7. Steward approves or rejects with notes.
8. Approved version becomes visible as the current version and available to downstream consumers.

## Acceptance criteria

- A user can find a schema by name, owner, domain, tag, type, or status.
- A contributor can create a draft schema version and see validation errors before submission.
- A steward can approve or reject a submitted schema version with decision notes.
- Approved versions are immutable.
- Version history and audit events are visible to authorized users.
- Compatibility status is displayed for every submitted version where a previous approved version exists.
- Retired schemas remain discoverable with clear status and replacement guidance where available.

## Success metrics

- 80% of governed schemas are discoverable through the UI within the first adoption milestone.
- Median schema review time is less than two business days.
- Schema validation failures are detected before release for participating teams.
- Fewer schema-related questions are handled through ad hoc Slack or ticket threads.
- At least one production pipeline consumes schema registry metadata after MVP launch.

## Operational requirements

- Store schema content immutably by version.
- Store validation result, validator version, timestamp, and error details.
- Never delete approved schema versions through the UI.
- All lifecycle changes must be audit logged.
- Schema search index should update within a documented freshness window.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Users bypass registry and continue using raw files. | Integrate with CI or ingestion checks after the MVP is proven. |
| Validation messages are too technical for contributors. | Normalize errors into field, path, severity, and suggested action. |
| Compatibility rules differ by domain. | Make compatibility mode configurable per schema. |
| Too many schema formats delay launch. | Start with JSON Schema and Avro only. |

## Rollout plan

1. Seed registry with a small number of representative schemas.
2. Pilot with one producer team and one consumer team.
3. Validate review workflow and schema diff usefulness.
4. Add API or CI integration for one production pipeline.
5. Expand supported domains after governance and validation behavior stabilizes.

## Open questions

- Which schema formats are mandatory for the first production rollout?
- What compatibility modes must be supported on day one?
- Which teams own stewardship by domain?
- Should approval be required for all versions or only breaking changes?
- Which downstream systems should consume schema metadata first?
