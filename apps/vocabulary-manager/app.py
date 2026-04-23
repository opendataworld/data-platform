from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field


Status = Literal["draft", "approved", "published"]

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent.parent
VOCAB_STORAGE_DIR = REPO_ROOT / "data-platform" / "registries" / "vocabularies"
VOCAB_STORAGE_DIR.mkdir(parents=True, exist_ok=True)


class VocabularyTerm(BaseModel):
    term_id: str = Field(min_length=1)
    preferred_label: str = Field(min_length=1)
    synonyms: list[str] = Field(default_factory=list)
    definition: str = Field(default="")
    broader_terms: list[str] = Field(default_factory=list)
    narrower_terms: list[str] = Field(default_factory=list)
    related_terms: list[str] = Field(default_factory=list)


class VocabularyAsset(BaseModel):
    vocabulary_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    status: Status = "draft"
    terms: list[VocabularyTerm] = Field(default_factory=list)
    updated_at: str | None = None


class StatusUpdate(BaseModel):
    status: Status


def _vocab_path(vocabulary_id: str) -> Path:
    safe_id = vocabulary_id.strip().replace("/", "-")
    return VOCAB_STORAGE_DIR / f"{safe_id}.json"


def _save_vocab(vocab: VocabularyAsset) -> VocabularyAsset:
    vocab.updated_at = datetime.now(timezone.utc).isoformat()
    path = _vocab_path(vocab.vocabulary_id)
    path.write_text(json.dumps(vocab.model_dump(), indent=2) + "\n", encoding="utf-8")
    return vocab


def _load_vocab(vocabulary_id: str) -> VocabularyAsset:
    path = _vocab_path(vocabulary_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Vocabulary '{vocabulary_id}' not found")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return VocabularyAsset.model_validate(payload)


def _allowed_transition(current: Status, target: Status) -> bool:
    allowed = {
        "draft": {"draft", "approved"},
        "approved": {"approved", "published"},
        "published": {"published"},
    }
    return target in allowed[current]


def _as_csv(vocab: VocabularyAsset) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "term_id",
            "preferred_label",
            "synonyms",
            "definition",
            "broader_terms",
            "narrower_terms",
            "related_terms",
        ],
    )
    writer.writeheader()
    for term in vocab.terms:
        writer.writerow(
            {
                "term_id": term.term_id,
                "preferred_label": term.preferred_label,
                "synonyms": "|".join(term.synonyms),
                "definition": term.definition,
                "broader_terms": "|".join(term.broader_terms),
                "narrower_terms": "|".join(term.narrower_terms),
                "related_terms": "|".join(term.related_terms),
            }
        )
    return output.getvalue()


def _csv_terms(csv_text: str) -> list[VocabularyTerm]:
    reader = csv.DictReader(io.StringIO(csv_text))
    required = {"term_id", "preferred_label", "definition"}
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise HTTPException(status_code=400, detail=f"CSV missing columns: {sorted(missing)}")

    def parse_pipe(value: str | None) -> list[str]:
        return [item.strip() for item in (value or "").split("|") if item.strip()]

    terms: list[VocabularyTerm] = []
    for row in reader:
        terms.append(
            VocabularyTerm(
                term_id=(row.get("term_id") or "").strip(),
                preferred_label=(row.get("preferred_label") or "").strip(),
                synonyms=parse_pipe(row.get("synonyms")),
                definition=(row.get("definition") or "").strip(),
                broader_terms=parse_pipe(row.get("broader_terms")),
                narrower_terms=parse_pipe(row.get("narrower_terms")),
                related_terms=parse_pipe(row.get("related_terms")),
            )
        )
    return terms


app = FastAPI(title="OpenDataWorld Vocabulary Manager MVP", version="0.1.0")


@app.get("/")
def index() -> dict[str, str]:
    return {
        "product": "vocabulary-manager-mvp",
        "storage": str(VOCAB_STORAGE_DIR.relative_to(REPO_ROOT)),
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/vocabularies")
def list_vocabularies() -> list[dict[str, str | int | None]]:
    rows: list[dict[str, str | int | None]] = []
    for path in sorted(VOCAB_STORAGE_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows.append(
            {
                "vocabulary_id": payload.get("vocabulary_id", ""),
                "name": payload.get("name", ""),
                "version": payload.get("version", ""),
                "status": payload.get("status", "draft"),
                "term_count": len(payload.get("terms", [])),
                "updated_at": payload.get("updated_at"),
            }
        )
    return rows


@app.post("/vocabularies", response_model=VocabularyAsset)
def create_vocabulary(vocab: VocabularyAsset) -> VocabularyAsset:
    path = _vocab_path(vocab.vocabulary_id)
    if path.exists():
        raise HTTPException(status_code=409, detail="Vocabulary already exists")
    return _save_vocab(vocab)


@app.get("/vocabularies/{vocabulary_id}", response_model=VocabularyAsset)
def get_vocabulary(vocabulary_id: str) -> VocabularyAsset:
    return _load_vocab(vocabulary_id)


@app.put("/vocabularies/{vocabulary_id}", response_model=VocabularyAsset)
def upsert_vocabulary(vocabulary_id: str, vocab: VocabularyAsset) -> VocabularyAsset:
    if vocab.vocabulary_id != vocabulary_id:
        raise HTTPException(status_code=400, detail="Path vocabulary_id must match body vocabulary_id")
    return _save_vocab(vocab)


@app.post("/vocabularies/{vocabulary_id}/status", response_model=VocabularyAsset)
def update_status(vocabulary_id: str, body: StatusUpdate) -> VocabularyAsset:
    vocab = _load_vocab(vocabulary_id)
    if not _allowed_transition(vocab.status, body.status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition: {vocab.status} -> {body.status}",
        )
    vocab.status = body.status
    return _save_vocab(vocab)


@app.get("/vocabularies/{vocabulary_id}/export.json", response_model=VocabularyAsset)
def export_json(vocabulary_id: str) -> VocabularyAsset:
    return _load_vocab(vocabulary_id)


@app.get("/vocabularies/{vocabulary_id}/export.csv", response_class=PlainTextResponse)
def export_csv(vocabulary_id: str) -> str:
    vocab = _load_vocab(vocabulary_id)
    return _as_csv(vocab)


@app.post("/vocabularies/import/json", response_model=VocabularyAsset)
def import_json(vocab: VocabularyAsset) -> VocabularyAsset:
    return _save_vocab(vocab)


class CsvImportRequest(BaseModel):
    vocabulary_id: str
    name: str
    version: str
    status: Status = "draft"
    csv_data: str


@app.post("/vocabularies/import/csv", response_model=VocabularyAsset)
def import_csv(payload: CsvImportRequest) -> VocabularyAsset:
    terms = _csv_terms(payload.csv_data)
    vocab = VocabularyAsset(
        vocabulary_id=payload.vocabulary_id,
        name=payload.name,
        version=payload.version,
        status=payload.status,
        terms=terms,
    )
    return _save_vocab(vocab)
