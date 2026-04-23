from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from entity_store import EntityStore

BASE_DIR = Path(__file__).resolve().parent
store = EntityStore(BASE_DIR / "data")


class AppHandler(BaseHTTPRequestHandler):
    def _json_response(self, payload: dict | list, status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _text_response(self, body: str, content_type: str = "text/plain", status: int = 200) -> None:
        output = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(output)))
        self.end_headers()
        self.wfile.write(output)

    def _body_json(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            ui_path = BASE_DIR / "static" / "index.html"
            self._text_response(ui_path.read_text(), content_type="text/html")
            return

        if path == "/api/entities":
            results = store.search(
                q=query.get("q", [""])[0],
                status=query.get("status", [""])[0],
                entity_type=query.get("entity_type", [""])[0],
            )
            self._json_response(results)
            return

        if path.startswith("/api/entities/"):
            entity_id = path.split("/")[-1]
            entity = store.get_entity(entity_id)
            if entity is None:
                self._json_response({"error": "not found"}, status=404)
                return
            self._json_response(entity)
            return

        if path == "/api/export.json":
            self._text_response(store.export_json(), content_type="application/json")
            return

        if path == "/api/export.csv":
            self._text_response(store.export_csv(), content_type="text/csv")
            return

        self._json_response({"error": "route not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            payload = self._body_json()

            if path == "/api/entities":
                entity = store.save_entity(payload)
                self._json_response(entity, status=HTTPStatus.CREATED)
                return

            if path.startswith("/api/entities/") and path.endswith("/transition"):
                entity_id = path.split("/")[-2]
                status = payload.get("status", "")
                entity = store.transition_status(entity_id, status)
                self._json_response(entity, status=HTTPStatus.CREATED)
                return

            if path == "/api/import.json":
                if not isinstance(payload, list):
                    raise ValueError("payload must be a list")
                saved = store.import_json(payload)
                self._json_response(saved, status=HTTPStatus.CREATED)
                return

            self._json_response({"error": "route not found"}, status=404)
        except FileNotFoundError:
            self._json_response({"error": "not found"}, status=404)
        except Exception as exc:  # minimal MVP error handling
            self._json_response({"error": str(exc)}, status=400)


def run() -> None:
    host = "0.0.0.0"
    port = 8091
    httpd = ThreadingHTTPServer((host, port), AppHandler)
    print(f"Canonical Entity Directory MVP running on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
