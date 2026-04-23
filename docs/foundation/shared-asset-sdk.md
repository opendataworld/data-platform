# Shared Asset SDK (Foundation)

## What this is

A lightweight shared helper layer for product slices that persist JSON assets in GitHub-backed storage paths.

Location:
- `src/shared/assets/`

It currently provides reusable helpers for:
- common status validation (`draft`, `approved`, `published`)
- UTC timestamp generation (`now_iso`)
- safe asset-id normalization (`sanitize_asset_id`)
- JSON load/save wrappers with consistent behavior
- basic shared metadata parsing (`AssetMetadata.from_payload`)
- shared error classes for validation and not-found cases

## When to use it

Use this layer when building or updating a product slice that stores registry assets as JSON files in this repo.

Typical use cases:
- validating lifecycle status
- normalizing IDs used in file names
- reading/writing JSON assets consistently
- handling common validation and not-found errors

## What it should not become yet

Do **not** turn this into a full framework right now.

For now, this shared layer should remain:
- small
- practical
- extraction of already-repeated logic only
- focused on immediate product-slice velocity

Avoid adding:
- product-specific domain models
- orchestration/runtime abstractions
- heavy plugin systems

## Current state

Before this change, product slices duplicated common logic for:
- status validation
- timestamp creation
- JSON asset load/save
- ID/path normalization

## Recommended next state

- Keep all new slice-level asset persistence code using `src/shared/assets/`.
- Continue product-specific validation in each product app, but route shared file/status concerns through the SDK helpers.
- Add helper coverage only when duplication appears in at least 2 slices.

## Future state

- Add optional transition-policy helpers (status graph) if more slices need identical transition rules.
- Add optional typed asset envelope helpers only after registry contracts stabilize.
- Consider publishing this as an internal package once boundaries are stable across registries.

## PRD mismatch note

The task references `org/high-level-prd.md` as required input. That file is currently missing in this repository, so strict PRD validation could not be performed from the specified path.

Smallest correction:
- add `org/high-level-prd.md` to the repo Prompt Registry paths,
- or update task references to the actual canonical PRD location if it lives elsewhere.
