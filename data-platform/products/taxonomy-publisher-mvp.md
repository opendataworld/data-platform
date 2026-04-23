# Taxonomy Publisher MVP Prompt

Prompt Registry Rule:
Before execution, first save this prompt to the appropriate Prompt Registry location in GitHub and then read it back. Treat the GitHub-stored version as the canonical prompt. All outputs, revisions, reviews, and approved final versions must be logged and managed through GitHub only.

PRD Rule:
Before doing any work, read the org-wide PRD from the Prompt Registry and use it as the architectural source of truth. Do not contradict the PRD. If current repo reality differs from the PRD, identify the mismatch explicitly and propose a correction.

Repo:
opendataworld/data-platform

Prompt Registry Path:
data-platform/products/taxonomy-publisher-mvp.md

Related PRD:
org/high-level-prd.md

Related Prompt Assets:
- data-platform/bootstrap.md
- data-platform/overview.md
- shared/review-prompt.md
- agents/repo-builder-agent.md

Output Paths:
- apps/taxonomy-publisher/
- docs/products/taxonomy-publisher.md
- docs/products/taxonomy-publisher-roadmap.md
- reviews/products/taxonomy-publisher-review.md

Objective:
Build the first real OpenDataWorld product: a thin **Taxonomy Publisher MVP** that lets users manage, version, review, and publish taxonomies using GitHub as the storage and versioning layer.

Product Intent:
This is a real product slice, not just platform infrastructure.
It should demonstrate the platform direction by making one governed data asset type useful end-to-end.

Scope of MVP:
- taxonomy asset stored in GitHub
- taxonomy metadata and versioning
- draft / approved / published states
- import/export in simple formats such as JSON and CSV
- minimal browser-accessible UI or API surface
- docs explaining usage, structure, and next steps

Current State:
- OpenDataWorld Data Platform umbrella repo exists
- Prompt Registry exists
- High-level PRD exists
- AGENTS.md exists
- Platform structure is being clarified
- No narrow product slice is yet established as the first working data product

Target State:
- There is a real `taxonomy-publisher` product slice in the repo
- It is small but usable
- It uses GitHub-backed assets and versioning
- It aligns with the platform architecture
- It leaves the repo cleaner and more product-oriented

Required Work:
1. Inspect the repo and determine the smallest clean product implementation approach
2. Create a new product slice under:
   - `apps/taxonomy-publisher/` or another justified product path
3. Define a minimal taxonomy asset model, including:
   - taxonomy id
   - name
   - version
   - status
   - terms/categories
   - parent-child relationships if applicable
   - aliases/labels if practical
4. Define a GitHub-backed storage convention for taxonomy assets
5. Build the smallest useful product surface, such as:
   - a minimal API
   - a minimal UI
   - or both, if already practical in the repo context
6. Add import/export support for simple formats:
   - JSON
   - CSV if practical
7. Support lifecycle states at minimum:
   - draft
   - approved
   - published
8. Write:
   - `docs/products/taxonomy-publisher.md`
   - `docs/products/taxonomy-publisher-roadmap.md`
9. Log review notes in:
   - `reviews/products/taxonomy-publisher-review.md`

Rules:
- Ship a usable thin product
- Do not overbuild a full taxonomy platform
- Keep the implementation small and clear
- Use GitHub as the asset/versioning layer
- Update structure/docs only as needed to support this product
- Prefer practical functionality over architecture theater
- Clearly separate current MVP from future roadmap

Important architectural constraint:
This is a product slice inside the Data Platform umbrella repo.
Do not prematurely split it into its own repo unless absolutely necessary.
Design it so it can become a future `taxonomy-registry` or product repo later if needed.

Expected Deliverables:
1. Product slice folder
2. Minimal working implementation
3. Taxonomy asset format/spec
4. Product docs
5. Review note
6. Clear future roadmap

Final Output Format:
1. Summary
2. Files created/updated
3. Product behavior delivered
4. Architectural decisions
5. Remaining follow-ups
