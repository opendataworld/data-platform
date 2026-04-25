# Registries

The `registries` domain contains the product and data assets used to manage reusable data-platform metadata: vocabularies, taxonomies, schemas, canonical entities, and publishing workflows.

## Folder structure

```text
data-platform/registries/
├── README.md
├── products/
│   ├── README.md
│   ├── canonical-entity-directory/
│   │   └── README.md
│   ├── schema-registry-ui/
│   │   └── README.md
│   ├── taxonomy-publisher/
│   │   └── README.md
│   └── vocabulary-manager/
│       └── README.md
└── vocabularies/
    └── example-core-science-vocab.json
```

## Conventions

- Product documentation lives under `products/<product-slug>/README.md`.
- Product folders are long-lived ownership boundaries, not milestone folders.
- Use additional subfolders such as `adr/`, `ux/`, `api/`, `release-notes/`, and `runbooks/` when a product needs deeper artifacts.
- Registry data examples live under the registry type they represent, such as `vocabularies/`.
- Use kebab-case for folder and file names.
- Keep generated artifacts, screenshots, exports, and environment-specific files out of this folder unless they are deliberate fixtures.

## Product areas

| Product | Purpose | Document |
| --- | --- | --- |
| Canonical Entity Directory | Maintains trusted entity records, identifiers, aliases, relationships, lifecycle states, and resolution APIs. | `products/canonical-entity-directory/README.md` |
| Schema Registry UI | Lets teams discover, validate, review, approve, compare, and operate schema contracts. | `products/schema-registry-ui/README.md` |
| Taxonomy Publisher | Publishes approved taxonomies as versioned, validated, immutable downstream artifacts. | `products/taxonomy-publisher/README.md` |
| Vocabulary Manager | Manages controlled vocabularies, terms, definitions, synonyms, relationships, and lifecycle governance. | `products/vocabulary-manager/README.md` |

## Documentation quality bar

A production-grade registry product document should define the product purpose, ownership model, target users, workflows, data contracts, permission model, lifecycle states, APIs, validation rules, integration points, operational requirements, security and privacy expectations, observability, failure modes, rollout plan, roadmap, and open decisions. The document should be detailed enough for product, design, engineering, data governance, and platform operations stakeholders to build and operate from without relying on tribal knowledge.
