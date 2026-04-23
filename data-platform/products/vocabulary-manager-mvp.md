# Prompt: Vocabulary Manager MVP

Prompt Registry Rule:
Before execution, first save this prompt to the appropriate Prompt Registry location in GitHub and then read it back. Treat the GitHub-stored version as the canonical prompt. All outputs, revisions, reviews, and approved final versions must be logged and managed through GitHub only.

PRD Rule:
Before doing any work, read the org-wide PRD from the Prompt Registry and use it as the architectural source of truth. Do not contradict the PRD. If current repo reality differs from the PRD, identify the mismatch explicitly and propose a correction.

Repo: opendataworld/data-platform
Prompt Registry Path: data-platform/products/vocabulary-manager-mvp.md
Related PRD: org/high-level-prd.md
Related Prompt Assets:
- data-platform/bootstrap.md
- data-platform/overview.md
- shared/review-prompt.md
- agents/repo-builder-agent.md

Output Paths:
- apps/vocabulary-manager/
- docs/products/vocabulary-manager.md
- docs/products/vocabulary-manager-roadmap.md
- reviews/products/vocabulary-manager-review.md

Objective:
Build a thin Vocabulary Manager MVP to manage/version/review/publish controlled vocabularies with GitHub as storage and versioning.

Required MVP scope:
- GitHub-backed vocabulary assets
- Metadata + versioning
- draft/approved/published lifecycle
- terms with preferred label, synonyms, definition
- JSON/CSV import-export
- minimal browser-accessible API/UI surface
- docs + roadmap + review note
