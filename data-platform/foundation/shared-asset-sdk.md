Prompt Registry Rule:
Before execution, first save this prompt to the appropriate Prompt Registry location in GitHub and then read it back. Treat the GitHub-stored version as the canonical prompt. All outputs, revisions, reviews, and approved final versions must be logged and managed through GitHub only.

PRD Rule:
Before doing any work, read the org-wide PRD from the Prompt Registry and use it as the architectural source of truth. Do not contradict the PRD. If current repo reality differs from the PRD, identify the mismatch explicitly and propose a correction.

Repo:
opendataworld/data-platform

Prompt Registry Path:
data-platform/foundation/shared-asset-sdk.md

Related PRD:
org/high-level-prd.md

Objective:
Build a small shared asset SDK/helper layer for the current OpenDataWorld product slices so they stop duplicating asset metadata handling, status handling, storage conventions, and GitHub-backed asset loading/saving behavior.

Context:
We now have multiple thin product slices and shared product templates. The next step is to extract the common asset-handling logic into one small reusable layer.

Tasks:
1. Inspect the current product slices and templates.
2. Identify duplicated logic across products for:
   - asset IDs
   - asset metadata
   - lifecycle/status handling
   - file path conventions
   - GitHub-backed storage/load/save behavior
   - validation helpers
3. Create a small shared layer, such as:
   - `src/shared/assets/`
   - or another justified path
4. Build reusable helpers for:
   - asset metadata parsing
   - asset status validation
   - file naming/path conventions
   - asset load/save helpers
   - common error handling
5. Keep the SDK/helper layer small and practical.
6. Refactor current product slices only as needed to use the shared layer.
7. Add docs explaining:
   - what the shared asset layer is
   - when to use it
   - what it should not become yet
8. Log review notes in:
   - reviews/foundation/shared-asset-sdk-review.md

Expected Outputs:
- shared asset helper layer
- small refactors in current products to use it
- docs/foundation/shared-asset-sdk.md
- review note

Rules:
- Do not overbuild a framework
- Keep it lightweight and immediately useful
- Extract only what is already repeated
- Preserve GitHub-backed asset storage as the operating model
- Keep current products working
- Make future product slices faster to build

Final Output Format:
1. Summary
2. Shared patterns extracted
3. Files created/updated
4. Product slices updated
5. Remaining follow-ups
