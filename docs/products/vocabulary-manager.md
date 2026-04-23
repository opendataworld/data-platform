# Vocabulary Manager MVP

## Product summary

Vocabulary Manager MVP is the second real OpenDataWorld product slice. It provides a small API-first surface for governed vocabulary management backed directly by GitHub/Git in this repository.

## Current state (implemented now)

- Product slice exists at `apps/vocabulary-manager/`.
- Vocabulary assets are JSON files stored in `data-platform/registries/vocabularies/`.
- API supports CRUD-style workflows, lifecycle state transitions, and import/export.
- Asset lifecycle uses these states:
  - `draft`
  - `approved`
  - `published`

## Vocabulary asset model

Each vocabulary asset includes:

- `vocabulary_id` (string)
- `name` (string)
- `version` (string)
- `status` (`draft | approved | published`)
- `terms` (array)
  - `term_id`
  - `preferred_label`
  - `synonyms` (string array)
  - `definition`
  - optional relationships:
    - `broader_terms`
    - `narrower_terms`
    - `related_terms`
- `updated_at` (ISO timestamp)

## GitHub-backed storage and versioning convention

- Canonical storage path:
  - `data-platform/registries/vocabularies/<vocabulary_id>.json`
- GitHub pull requests, reviews, and commit history provide:
  - diff visibility
  - approval workflow
  - rollback
  - publish traceability

This keeps the MVP aligned with the data-platform umbrella repo and avoids premature repo splitting.

## API behavior delivered

Base service: FastAPI app in `apps/vocabulary-manager/app.py`

Endpoints:

- `GET /` – product metadata and storage path
- `GET /health` – health check
- `GET /vocabularies` – list vocabulary summaries
- `POST /vocabularies` – create vocabulary
- `GET /vocabularies/{id}` – fetch vocabulary
- `PUT /vocabularies/{id}` – update vocabulary
- `POST /vocabularies/{id}/status` – state transitions (`draft->approved->published`)
- `GET /vocabularies/{id}/export.json` – JSON export
- `GET /vocabularies/{id}/export.csv` – CSV export
- `POST /vocabularies/import/json` – JSON import
- `POST /vocabularies/import/csv` – CSV import

## CSV format

Supported columns:

- `term_id`
- `preferred_label`
- `synonyms` (pipe-delimited)
- `definition`
- `broader_terms` (pipe-delimited)
- `narrower_terms` (pipe-delimited)
- `related_terms` (pipe-delimited)

## Minimal usage

Run locally:

```bash
cd apps/vocabulary-manager
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8090
```

Open Swagger UI at `http://127.0.0.1:8090/docs`.

## Architectural alignment notes

- Product remains inside the umbrella repo per current architecture direction.
- GitHub is used as storage/versioning via repository file assets and commits.
- Scope is intentionally thin to deliver one governed asset type end-to-end.
