# Vocabulary Manager MVP

Thin product slice for managing controlled vocabularies as Git-tracked JSON assets in this repository.

## Run

```bash
cd apps/vocabulary-manager
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8090
```

Open:
- API root: `http://127.0.0.1:8090/`
- Swagger UI: `http://127.0.0.1:8090/docs`

## Status model

- `draft` -> `approved` -> `published`

## Storage convention

Vocabulary assets are persisted to:

- `data-platform/registries/vocabularies/<vocabulary_id>.json`

This keeps assets in GitHub for review, history, rollback, and publishing workflows.
