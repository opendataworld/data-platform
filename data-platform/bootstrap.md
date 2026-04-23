# Bootstrap Prompt: Reposition OpenDataWorld Data Platform Umbrella Repo

Prompt Registry Rule:
Before execution, first save this prompt to the appropriate Prompt Registry location in GitHub and then read it back. Treat the GitHub-stored version as the canonical prompt. All outputs, revisions, reviews, and approved final versions must be logged and managed through GitHub only.

PRD Rule:
Before doing any work, read the org-wide PRD from the Prompt Registry and use it as the architectural source of truth. Do not contradict the PRD. If current repo reality differs from the PRD, identify the mismatch explicitly and propose a correction.

Repo:
opendataworld/data-platform

Prompt Registry Path:
data-platform/bootstrap.md

Related PRD:
org/high-level-prd.md

Output Paths:
- README.md
- docs/platform-overview.md
- docs/module-map.md
- docs/upstream-strategy.md
- docs/repo-roadmap.md
- reviews/data-platform/bootstrap-review.md

Objective:
Reposition `opendataworld/data-platform` as the umbrella repo for the OpenDataWorld Data Platform and make the repo structure, documentation, and platform narrative consistent with the PRD.

Current State:
- The repo is already an umbrella deployment repo with multiple OSS services and compose profiles.
- The README and docs do not yet fully reflect the clarified platform structure.
- The Data Platform vision now includes canonical domain registries, OSS-first integration, and a future modular split, but this should not be over-split yet.

Target State:
- The repo clearly presents OpenDataWorld as the Data Platform.
- The README explains current scope, planned modules, and relation to AgentNxt.
- The docs define the module map and future repo structure without prematurely splitting everything.
- The OSS strategy is explicit: integrate/compose first, fork only when necessary.
- The repo is cleaner and more understandable after the change.

Required Work:
1. Audit the existing README, docs, and compose/profile structure.
2. Rewrite README.md to:
   - position this repo as the OpenDataWorld Data Platform umbrella repo
   - explain current purpose and scope
   - explain relation to AgentNxt
   - explain canonical registries as the long-term architecture
   - explain current OSS foundations and planned additions like Marquez and Feast
3. Create:
   - docs/platform-overview.md
   - docs/module-map.md
   - docs/upstream-strategy.md
   - docs/repo-roadmap.md
4. In the docs, define these module meanings clearly:
   - catalog
   - lineage
   - ingestion
   - resolution
   - semantic
   - visualization
   - graph
   - store
   - labeling
   - features
   - search
   - docs
   - registries (future canonical domain registries)
5. Distinguish clearly between:
   - current state
   - recommended next state
   - future modular split
6. Do not aggressively create fake product claims or pretend separate repos already exist.
7. Leave review notes in:
   - reviews/data-platform/bootstrap-review.md

Rules:
- Build the product/repo clarity first
- Make only the minimum structural changes needed
- Prefer practical documentation and organization over abstract redesign
- Keep OpenDataWorld and AgentNxt clearly separate
- Do not rewrite OSS systems
- Keep changes reviewable

Deliverables:
1. Updated README.md
2. New docs files
3. Review note documenting:
   - what changed
   - what remains future work
   - any mismatches found between repo reality and PRD

Final Output Format:
1. Summary
2. Files created/updated
3. Key architecture decisions reflected
4. Remaining follow-ups
