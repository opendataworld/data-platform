# Registry Products

This folder contains product documentation for the registry capabilities in the data platform.

## Structure

Each product has its own folder:

```text
products/
├── canonical-entity-directory/
│   └── mvp.md
├── schema-registry-ui/
│   └── mvp.md
├── taxonomy-publisher/
│   └── mvp.md
└── vocabulary-manager/
    └── mvp.md
```

Use this structure instead of storing many loose product files directly under `products/`. It keeps product-specific artifacts colocated and makes it easier to add implementation notes, release plans, UX flows, diagrams, or ADRs later.

## Naming conventions

- Product folders use kebab-case.
- The MVP scope document is always `mvp.md`.
- Later product artifacts should use descriptive names such as `prd.md`, `roadmap.md`, `release-notes.md`, or `adr/<decision-title>.md`.

## Documentation quality bar

Every product document should answer:

1. What user or governance problem are we solving?
2. Who are the users and what jobs do they need to complete?
3. What is included in the MVP and what is explicitly out of scope?
4. What workflows, permissions, and data objects are required?
5. How will we know the product is working?
6. What operational, security, privacy, and adoption risks remain?
