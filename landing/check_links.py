#!/usr/bin/env python3
"""Check links in landing/index.html for basic production readiness."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


def extract_links(html: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', html)


def check_link(link: str, base: str | None = None, timeout: int = 10) -> tuple[bool, str]:
    if link.startswith("#") or link.startswith("mailto:") or link.startswith("tel:"):
        return True, "skipped (non-http link)"

    if not link.startswith(("http://", "https://")):
        if not base:
            return False, "relative link provided without --base"
        link = urljoin(base, link)

    try:
        req = Request(link, headers={"User-Agent": "odw-link-checker/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400, f"HTTP {resp.status}"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def main() -> int:
    html_path = Path(__file__).with_name("index.html")
    html = html_path.read_text(encoding="utf-8")
    links = extract_links(html)
    if not links:
        print("No links found.")
        return 1

    base_url = sys.argv[1] if len(sys.argv) > 1 else None
    failures = 0
    for link in links:
        ok, detail = check_link(link, base=base_url)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {link} -> {detail}")
        if not ok:
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
