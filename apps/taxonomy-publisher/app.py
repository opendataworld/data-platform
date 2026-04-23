#!/usr/bin/env python3
"""Taxonomy Publisher MVP: minimal API + UI with Git-tracked JSON storage."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shared.assets import ensure_status, read_asset_json, sanitize_asset_id, save_asset_json

STORAGE_DIR = APP_DIR / "storage" / "taxonomies"
STATIC_DIR = APP_DIR / "static"
VALID_STATUSES = {"draft", "approved", "published"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    return sanitize_asset_id(value)


def taxonomy_path(taxonomy_id: str) -> Path:
    return STORAGE_DIR / f"{slugify(taxonomy_id)}.json"


def validate_taxonomy(payload: dict[str, Any], allow_missing_core: bool = False) -> dict[str, Any]:
    taxonomy_id = payload.get("id")
    name = payload.get("name")
    if not allow_missing_core and (not taxonomy_id or not name):
        raise ValueError("taxonomy requires 'id' and 'name'")

    status = ensure_status(payload.get("status", "draft"), allowed_statuses=VALID_STATUSES)

    terms = payload.get("terms", [])
    if not isinstance(terms, list):
        raise ValueError("terms must be a list")

    normalized_terms: list[dict[str, Any]] = []
    for idx, term in enumerate(terms):
        if not isinstance(term, dict):
            raise ValueError(f"term index {idx} must be an object")
        term_id = term.get("id") or f"term-{idx + 1}"
        label = term.get("label")
        if not label:
            raise ValueError(f"term '{term_id}' missing required field 'label'")
        aliases = term.get("aliases", [])
        if aliases and not isinstance(aliases, list):
            raise ValueError(f"term '{term_id}' aliases must be a list")
        normalized_terms.append(
            {
                "id": slugify(str(term_id)),
                "label": str(label),
                "parent_id": slugify(str(term["parent_id"])) if term.get("parent_id") else None,
                "aliases": [str(alias) for alias in aliases],
            }
        )

    version = payload.get("version", "0.1.0")
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be an object")

    created_at = payload.get("created_at") or now_iso()
    updated_at = now_iso()

    return {
        "id": slugify(str(taxonomy_id or "")),
        "name": str(name or ""),
        "version": str(version),
        "status": status,
        "terms": normalized_terms,
        "metadata": metadata,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def read_taxonomy(taxonomy_id: str) -> dict[str, Any]:
    path = taxonomy_path(taxonomy_id)
    if not path.exists():
        raise FileNotFoundError(f"taxonomy '{taxonomy_id}' does not exist")
    return read_asset_json(path)


def write_taxonomy(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = validate_taxonomy(payload)
    save_asset_json(taxonomy_path(normalized["id"]), normalized)
    return normalized


def list_taxonomies(status: str | None = None) -> list[dict[str, Any]]:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    items: list[dict[str, Any]] = []
    for path in sorted(STORAGE_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as fh:
            item = json.load(fh)
        if status and item.get("status") != status:
            continue
        items.append(item)
    return items


def taxonomy_to_csv_rows(taxonomy: dict[str, Any]) -> list[list[str]]:
    rows = [["taxonomy_id", "taxonomy_name", "taxonomy_version", "status", "term_id", "label", "parent_id", "aliases"]]
    for term in taxonomy.get("terms", []):
        rows.append(
            [
                taxonomy.get("id", ""),
                taxonomy.get("name", ""),
                taxonomy.get("version", ""),
                taxonomy.get("status", ""),
                term.get("id", ""),
                term.get("label", ""),
                term.get("parent_id") or "",
                "|".join(term.get("aliases") or []),
            ]
        )
    return rows


def csv_text_to_taxonomy(csv_text: str) -> dict[str, Any]:
    reader = csv.DictReader(csv_text.splitlines())
    terms: list[dict[str, Any]] = []
    base: dict[str, Any] = {}
    for row in reader:
        if not base:
            base = {
                "id": row.get("taxonomy_id", ""),
                "name": row.get("taxonomy_name", ""),
                "version": row.get("taxonomy_version") or "0.1.0",
                "status": row.get("status") or "draft",
            }
        aliases = row.get("aliases", "")
        terms.append(
            {
                "id": row.get("term_id") or None,
                "label": row.get("label") or "",
                "parent_id": row.get("parent_id") or None,
                "aliases": [a for a in aliases.split("|") if a],
            }
        )
    if not base:
        raise ValueError("csv payload was empty")
    base["terms"] = terms
    return validate_taxonomy(base)


class Handler(BaseHTTPRequestHandler):
    server_version = "TaxonomyPublisherMVP/0.1"

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_text(self, payload: str, content_type: str = "text/plain; charset=utf-8", status: HTTPStatus = HTTPStatus.OK) -> None:
        data = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        if not raw.strip():
            return {}
        return json.loads(raw)

    def _read_text_body(self) -> str:
        length = int(self.headers.get("Content-Length", "0"))
        return self.rfile.read(length).decode("utf-8")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
            return self._send_text(html, content_type="text/html; charset=utf-8")

        if parsed.path == "/health":
            return self._send_json({"status": "ok", "service": "taxonomy-publisher-mvp"})

        if parsed.path == "/api/taxonomies":
            params = parse_qs(parsed.query)
            status = params.get("status", [None])[0]
            if status and status not in VALID_STATUSES:
                return self._send_json({"error": f"invalid status '{status}'"}, HTTPStatus.BAD_REQUEST)
            return self._send_json({"items": list_taxonomies(status=status)})

        if parsed.path.startswith("/api/taxonomies/"):
            suffix = parsed.path.removeprefix("/api/taxonomies/")
            if suffix.endswith("/export.csv"):
                taxonomy_id = suffix.removesuffix("/export.csv")
                try:
                    taxonomy = read_taxonomy(taxonomy_id)
                except FileNotFoundError as exc:
                    return self._send_json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
                rows = taxonomy_to_csv_rows(taxonomy)
                output = []
                for row in rows:
                    output.append(",".join([f'"{col.replace("\"", "\"\"")}"' for col in row]))
                return self._send_text("\n".join(output) + "\n", content_type="text/csv; charset=utf-8")

            taxonomy_id = suffix
            try:
                taxonomy = read_taxonomy(taxonomy_id)
            except FileNotFoundError as exc:
                return self._send_json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
            return self._send_json(taxonomy)

        return self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/taxonomies":
            try:
                payload = self._read_json_body()
                created = write_taxonomy(payload)
                return self._send_json(created, HTTPStatus.CREATED)
            except (ValueError, json.JSONDecodeError) as exc:
                return self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        if parsed.path == "/api/import/csv":
            try:
                payload = self._read_text_body()
                taxonomy = csv_text_to_taxonomy(payload)
                saved = write_taxonomy(taxonomy)
                return self._send_json(saved, HTTPStatus.CREATED)
            except ValueError as exc:
                return self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        return self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_PUT(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/taxonomies/"):
            taxonomy_id = parsed.path.removeprefix("/api/taxonomies/")
            try:
                existing = read_taxonomy(taxonomy_id)
                patch = self._read_json_body()
                merged = {**existing, **patch, "id": taxonomy_id}
                saved = write_taxonomy(merged)
                return self._send_json(saved)
            except FileNotFoundError as exc:
                return self._send_json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
            except (ValueError, json.JSONDecodeError) as exc:
                return self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        return self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", 8787), Handler)
    print("Taxonomy Publisher MVP listening on http://0.0.0.0:8787")
    server.serve_forever()
