# Shared Product Patterns Prompt (Canonical)

Saved: 2026-04-23 (UTC)
Source: user task prompt in Codex session

## Prompt

Prompt Registry Rule:
Before execution, first save this prompt to the appropriate Prompt Registry location in GitHub and then read it back. Treat the GitHub-stored version as the canonical prompt. All outputs, revisions, reviews, and approved final versions must be logged and managed through GitHub only.

PRD Rule:
Before doing any work, read the org-wide PRD from the Prompt Registry and use it as the architectural source of truth. Do not contradict the PRD. If current repo reality differs from the PRD, identify the mismatch explicitly and propose a correction.

Repo: `opendataworld/data-platform`

Prompt Registry Path: `data-platform/templates/shared-product-patterns.md`

Related PRD: `org/high-level-prd.md`

Objective:
Extract the common patterns from the completed and consolidated product slices, and convert them into shared product templates and conventions for future OpenDataWorld products.

Tasks:
1. Inspect consolidated slices for common patterns (folder structure, metadata format, lifecycle model, GitHub-backed storage, docs structure, review format, app/API/UI shape).
2. Define a standard reusable product template for future slices.
3. Create shared templates and conventions for product folders, assets, metadata/frontmatter schema, status model, product docs, roadmap docs, and review notes.
4. Add docs for building the next slice with the pattern.
5. Create template files under shared template paths.
6. Normalize existing slices with small changes if needed.
7. Log review notes in `reviews/templates/shared-product-patterns-review.md`.

Expected Outputs:
- `docs/product-template.md`
- `templates/product/README-template.md`
- `templates/product/roadmap-template.md`
- `templates/product/review-template.md`
- `templates/assets/asset-template.json`
- `templates/assets/asset-template.yaml`
- Small normalization updates in current slices as needed
- Review notes

Rules:
- Keep the pattern simple and reusable
- Avoid overengineering
- Base the pattern on what worked in existing slices
- Prefer consistency and reuse
- Keep GitHub-backed asset storage central
- Make future product creation faster
