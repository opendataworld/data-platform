# Taxonomy Publisher MVP

## Status

- **Product area:** Registries
- **Lifecycle stage:** MVP definition
- **Primary users:** Taxonomy stewards, data governance teams, platform engineers, search/recommendation consumers, analytics teams
- **Primary outcome:** Publish approved taxonomies as versioned, validated, machine-readable artifacts that downstream systems can reliably consume.

## Problem statement

Taxonomies often start as spreadsheets, documents, or isolated configuration files. That makes it hard to know which taxonomy version is approved, when it changed, whether downstream systems have received it, and whether the structure is valid. The MVP creates a controlled publishing workflow that turns approved taxonomy drafts into versioned artifacts with validation, metadata, audit history, and delivery status.

## Goals

- Publish approved taxonomy versions through a repeatable governed workflow.
- Validate taxonomy structure before publication.
- Provide stable versioned artifacts for downstream consumers.
- Track publication status, destination delivery, and audit history.
- Support rollback or deprecation without deleting previously published artifacts.

## Non-goals

- Advanced taxonomy authoring UI.
- Automated ontology reasoning or inference.
- Real-time collaborative editing.
- Complex taxonomy visualization beyond a simple hierarchy preview.
- Direct customization for every downstream consumer format on day one.

## MVP users and jobs

| User | Job to be done |
| --- | --- |
| Taxonomy steward | Review and publish an approved taxonomy version. |
| Governance administrator | Configure publishing destinations, approval rules, and required metadata. |
| Platform engineer | Integrate published taxonomy artifacts into services and pipelines. |
| Search or recommendation consumer | Retrieve the latest approved taxonomy in a predictable format. |
| Analyst | Confirm which taxonomy version was active for a report or model. |

## MVP scope

### Taxonomy publication

- Select an approved taxonomy draft for publication.
- Validate required metadata, hierarchy integrity, unique identifiers, and status values.
- Assign a semantic version or platform-generated version.
- Publish immutable taxonomy artifact files.
- Mark a published version as current, deprecated, or retired.

### Validation

- Detect missing required fields.
- Detect duplicate node identifiers.
- Detect cycles in hierarchical relationships.
- Detect references to missing parent or related nodes.
- Detect invalid lifecycle statuses.
- Produce validation results with severity, message, node reference, and remediation guidance.

### Delivery

- Publish artifacts to configured storage or registry destinations.
- Generate a manifest with artifact metadata, content hash, published timestamp, and publisher.
- Expose latest and version-specific retrieval paths.
- Track destination delivery status.

### Audit and governance

- Require approval before publication.
- Capture publisher, timestamp, source draft, version, validation result, and change summary.
- Prevent mutation of published versions.
- Support deprecation with required reason and optional replacement version.

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| TP-001 | Users can view taxonomy drafts eligible for publication. | Must |
| TP-002 | The system validates taxonomy structure before publication. | Must |
| TP-003 | Users can publish an approved taxonomy as an immutable versioned artifact. | Must |
| TP-004 | Publication creates a manifest with version, hash, status, and timestamp. | Must |
| TP-005 | Consumers can retrieve latest and version-specific taxonomy artifacts. | Must |
| TP-006 | Published versions can be deprecated or retired without deletion. | Must |
| TP-007 | The system tracks publishing destination delivery status. | Should |
| TP-008 | Users can compare published taxonomy versions. | Should |
| TP-009 | The system emits publication events for downstream subscribers. | Should |
| TP-010 | Users can download published artifacts from the UI. | Could |

## Artifact contract

Each publication should produce at least two artifacts:

1. `taxonomy.json` containing taxonomy nodes and relationships.
2. `manifest.json` containing publication metadata.

Example manifest:

```json
{
  "taxonomy_id": "tax_research_domains",
  "name": "Research Domains",
  "version": "1.0.0",
  "status": "current",
  "content_hash": "sha256:...",
  "source_draft_id": "draft_01HZX7K9E2F3M4N5P6Q7R8S9T0",
  "published_at": "2026-04-25T00:00:00Z",
  "published_by": "steward@example.org",
  "validation_status": "passed",
  "artifact_paths": {
    "versioned": "registries/taxonomies/research-domains/1.0.0/taxonomy.json",
    "latest": "registries/taxonomies/research-domains/latest/taxonomy.json"
  }
}
```

## Minimum taxonomy node model

```json
{
  "node_id": "biology",
  "preferred_label": "Biology",
  "definition": "The study of living organisms and their interactions.",
  "status": "active",
  "parent_node_id": "science",
  "aliases": ["life science"],
  "related_node_ids": ["ecology"],
  "sort_order": 10
}
```

## Permissions

| Role | Capabilities |
| --- | --- |
| Viewer | View and download published taxonomies. |
| Contributor | Prepare taxonomy drafts in the source authoring system. |
| Publisher | Validate and publish approved taxonomy versions. |
| Steward | Approve, deprecate, retire, and mark current versions. |
| Administrator | Configure destinations, required metadata, and role mappings. |

## Workflow

1. Contributor prepares or imports taxonomy draft in the source authoring workflow.
2. Steward approves the draft for publication.
3. Publisher selects the approved draft and runs validation.
4. System blocks publication if must-fix validation errors exist.
5. Publisher assigns version and confirms release notes.
6. System writes immutable artifacts and manifest.
7. System updates the latest pointer if the new version is current.
8. Downstream systems retrieve the artifact or receive publication events.
9. Older versions remain available for reproducibility.

## Acceptance criteria

- An approved taxonomy can be validated and published as a versioned immutable artifact.
- Publication fails when required metadata is missing, node IDs are duplicated, cycles exist, or parent references are invalid.
- Every published taxonomy includes a manifest with version, hash, status, publisher, timestamp, and artifact path.
- Consumers can retrieve the latest current version and a specific historical version.
- Deprecating or retiring a taxonomy does not delete published artifacts.
- Publication, deprecation, and retirement actions are audit logged.

## Success metrics

- 100% of published taxonomies include valid manifests.
- Failed publications caused by structural validation errors decrease after initial onboarding.
- Downstream consumers can migrate from manual taxonomy files to published artifact paths.
- Median time from steward approval to published artifact is less than one business day.
- No published artifact is overwritten after release.

## Operational requirements

- Published artifacts must be immutable.
- Latest pointers must update atomically with the publication manifest.
- Content hash must be calculated after artifact generation.
- Publication jobs must be idempotent or safely retryable.
- Delivery status must clearly distinguish validation failure, artifact write failure, and downstream delivery failure.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Taxonomy source systems vary widely. | Define a strict import contract and normalize before publishing. |
| Consumers depend on unversioned latest paths only. | Provide both latest and version-specific paths and document usage. |
| Invalid hierarchy breaks downstream systems. | Block publication on cycles, missing parents, and duplicate IDs. |
| Rollback expectations conflict with immutability. | Use current pointer changes and deprecation instead of artifact mutation. |

## Rollout plan

1. Publish one low-risk taxonomy as a pilot.
2. Integrate one downstream consumer using version-specific artifact retrieval.
3. Add latest pointer consumption after versioned retrieval is proven.
4. Expand to priority governed taxonomies.
5. Add event delivery or destination tracking for production consumers.

## Open questions

- Which taxonomy authoring source is canonical for MVP input?
- What versioning policy should be enforced?
- Which artifact destination should be the first production target?
- Are publication approvals separate from taxonomy content approvals?
- Which consumers require event notifications instead of polling?
