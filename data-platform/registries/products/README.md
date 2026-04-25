# Registry Products

This folder contains production-grade product documentation for registry capabilities in the data platform.

## Structure

Each product owns a folder with a primary `README.md`:

```text
products/
├── canonical-entity-directory/
│   └── README.md
├── schema-registry-ui/
│   └── README.md
├── taxonomy-publisher/
│   └── README.md
└── vocabulary-manager/
    └── README.md
```

Use this structure instead of storing many loose files directly under `products/`. Product folders are stable ownership boundaries and can later contain `adr/`, `ux/`, `api/`, `runbooks/`, `fixtures/`, and `release-notes/`.

## Product documents

| Product | Document | Core responsibility |
| --- | --- | --- |
| Canonical Entity Directory | `canonical-entity-directory/README.md` | Canonical IDs, aliases, external identifiers, entity lifecycle, entity resolution, and downstream reference safety. |
| Schema Registry UI | `schema-registry-ui/README.md` | Schema discovery, validation, version comparison, approval, compatibility, and contract governance. |
| Taxonomy Publisher | `taxonomy-publisher/README.md` | Validation, immutable taxonomy publication, manifests, artifact delivery, lifecycle events, and downstream consumption. |
| Vocabulary Manager | `vocabulary-manager/README.md` | Controlled vocabulary authoring, term governance, definitions, synonyms, relationships, import/export, and lifecycle management. |

## Documentation quality bar

Each product README should include:

- Product purpose and problem statement
- Operating principles and product boundaries
- Users, roles, and responsibilities
- Production workflows and lifecycle states
- Functional capabilities and non-functional requirements
- Data model and artifact contracts
- API surface and integration points
- Permissions, security, privacy, and audit expectations
- Validation rules and failure handling
- Observability and operational runbook expectations
- Rollout, migration, adoption, and roadmap guidance
- Open decisions and explicit assumptions
