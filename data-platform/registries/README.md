# Registries

The `registries` domain contains the product and data assets used to manage reusable data-platform metadata: vocabularies, taxonomies, schemas, canonical entities, and publishing workflows.

## Folder structure

```text
data-platform/registries/
├── README.md
├── products/
│   ├── README.md
│   ├── canonical-entity-directory/
│   │   └── mvp.md
│   ├── schema-registry-ui/
│   │   └── mvp.md
│   ├── taxonomy-publisher/
│   │   └── mvp.md
│   └── vocabulary-manager/
│       └── mvp.md
└── vocabularies/
    └── example-core-science-vocab.json
```

## Conventions

- Product discovery and delivery documents live under `products/<product-slug>/`.
- MVP documents are named `mvp.md` so each product can later add `prd.md`, `roadmap.md`, `adr/`, `ux/`, and `release-notes/` without renaming the original artifact.
- Registry data examples live under the registry type they represent, such as `vocabularies/`.
- Use kebab-case for folder and file names.
- Keep generated artifacts, screenshots, exports, and environment-specific files out of this folder unless they are deliberate fixtures.

## Product areas

| Product | Purpose | MVP document |
| --- | --- | --- |
| Canonical Entity Directory | Maintains trusted entity records and identifiers across datasets. | `products/canonical-entity-directory/mvp.md` |
| Schema Registry UI | Lets teams discover, review, validate, and govern schemas. | `products/schema-registry-ui/mvp.md` |
| Taxonomy Publisher | Publishes approved taxonomies to versioned downstream consumers. | `products/taxonomy-publisher/mvp.md` |
| Vocabulary Manager | Manages controlled vocabularies, terms, synonyms, and definitions. | `products/vocabulary-manager/mvp.md` |

## Definition of production-ready documentation

A registry product document should define the user problem, target users, MVP scope, non-goals, functional requirements, data model, permissions, workflows, success metrics, risks, rollout plan, and open questions. Product docs should be specific enough for design, engineering, and data-governance stakeholders to estimate and build from without relying on tribal knowledge.
