# Parallel Run Consolidation Prompt (Canonical)

Saved: 2026-04-23 (UTC)
Source: user task prompt in Codex session

## Prompt Registry Rule
Before execution, first save this prompt to the appropriate Prompt Registry location in GitHub and then read it back. Treat the GitHub-stored version as the canonical prompt. All outputs, revisions, reviews, and approved final versions must be logged and managed through GitHub only.

## PRD Rule
Before doing any work, read the org-wide PRD from the Prompt Registry and use it as the architectural source of truth. Do not contradict the PRD. If current repo reality differs from the PRD, identify the mismatch explicitly and propose a correction.

## Repo
`opendataworld/data-platform`

## Prompt Registry Path
`data-platform/reviews/parallel-run-consolidation.md`

## Related PRD
`org/high-level-prd.md`

## Objective
Review and consolidate the outputs of the 4 parallel prompt runs for the OpenDataWorld Data Platform.

## Tasks
1. Inspect all changes produced by the 4 parallel runs.
2. Identify:
   - overlaps
   - conflicts
   - duplicate files
   - inconsistent naming
   - inconsistent architecture assumptions
   - mismatches with the PRD
3. Propose the cleanest merged state.
4. Keep the best parts of each change set.
5. Normalize:
   - README language
   - docs structure
   - product folder structure
   - asset naming
   - status/lifecycle naming
6. Produce:
   - a consolidation summary
   - a merge plan
   - a recommended final file structure
   - a list of changes to accept, modify, or reject
7. Write review notes to:
   - `reviews/parallel-run-consolidation-review.md`

## Rules
- Do not blindly merge everything
- Prefer consistency over volume
- Keep the repo small and coherent
- Align everything to the PRD and AGENTS.md
- Distinguish current accepted state vs deferred future work

## Final Output Format
1. Summary
2. Conflicts found
3. Best changes to keep
4. Changes to reject or modify
5. Recommended final merged structure
6. Remaining follow-ups
