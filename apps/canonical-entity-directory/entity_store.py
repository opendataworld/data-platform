from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shared.assets import ensure_status, now_iso, read_asset_json, save_asset_json

VALID_STATUS = {"draft", "approved", "published"}


@dataclass
class EntityStore:
    root: Path

    @property
    def entities_root(self) -> Path:
        return self.root / "entities"

    def list_entities(self) -> list[dict[str, Any]]:
        entities: list[dict[str, Any]] = []
        if not self.entities_root.exists():
            return entities

        for entity_dir in sorted(self.entities_root.iterdir()):
            latest = entity_dir / "latest.json"
            if latest.exists():
                entities.append(read_asset_json(latest))
        return entities

    def get_entity(self, entity_id: str) -> dict[str, Any] | None:
        path = self.entities_root / entity_id / "latest.json"
        if path.exists():
            return read_asset_json(path)
        return None

    def save_entity(self, payload: dict[str, Any]) -> dict[str, Any]:
        entity_id = payload["entity_id"].strip()
        if not entity_id:
            raise ValueError("entity_id is required")

        existing = self.get_entity(entity_id)
        next_version = 1 if existing is None else int(existing["version"]) + 1

        status = ensure_status(payload.get("status", "draft"), allowed_statuses=VALID_STATUS)

        entity = {
            "entity_id": entity_id,
            "canonical_name": payload["canonical_name"].strip(),
            "entity_type": payload["entity_type"].strip(),
            "version": next_version,
            "status": status,
            "aliases": [a.strip() for a in payload.get("aliases", []) if a.strip()],
            "source_references": [s.strip() for s in payload.get("source_references", []) if s.strip()],
            "description": payload.get("description", "").strip(),
            "notes": payload.get("notes", "").strip(),
            "updated_at": now_iso(),
        }

        entity_dir = self.entities_root / entity_id
        entity_dir.mkdir(parents=True, exist_ok=True)
        version_path = entity_dir / f"v{next_version}.json"
        latest_path = entity_dir / "latest.json"
        save_asset_json(version_path, entity)
        save_asset_json(latest_path, entity)
        return entity

    def transition_status(self, entity_id: str, status: str) -> dict[str, Any]:
        status = ensure_status(status, allowed_statuses=VALID_STATUS)

        entity = self.get_entity(entity_id)
        if not entity:
            raise FileNotFoundError(entity_id)

        entity["status"] = status
        return self.save_entity(entity)

    def search(self, q: str = "", status: str = "", entity_type: str = "") -> list[dict[str, Any]]:
        results = []
        needle = q.lower().strip()

        for entity in self.list_entities():
            if status and entity["status"] != status:
                continue
            if entity_type and entity["entity_type"] != entity_type:
                continue

            searchable = " ".join(
                [
                    entity["entity_id"],
                    entity["canonical_name"],
                    entity["entity_type"],
                    " ".join(entity.get("aliases", [])),
                    " ".join(entity.get("source_references", [])),
                ]
            ).lower()
            if needle and needle not in searchable:
                continue
            results.append(entity)

        return results

    def export_json(self) -> str:
        return json.dumps(self.list_entities(), indent=2) + "\n"

    def export_csv(self) -> str:
        return self._dicts_to_csv(
            self.list_entities(),
            [
                "entity_id",
                "canonical_name",
                "entity_type",
                "version",
                "status",
                "aliases",
                "source_references",
                "description",
                "notes",
                "updated_at",
            ],
        )

    def _dicts_to_csv(self, rows: list[dict[str, Any]], headers: list[str]) -> str:
        from io import StringIO

        buf = StringIO()
        writer = csv.DictWriter(buf, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    "aliases": "|".join(row.get("aliases", [])),
                    "source_references": "|".join(row.get("source_references", [])),
                }
            )
        return buf.getvalue()

    def import_json(self, payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
        saved: list[dict[str, Any]] = []
        for entity in payload:
            saved.append(self.save_entity(entity))
        return saved
