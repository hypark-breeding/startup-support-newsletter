#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install with: python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "sources.yaml"

REQUIRED = {
    "id",
    "name",
    "name_ko",
    "region",
    "organization_type",
    "source_priority",
    "coverage_priority",
    "base_url",
    "entry_urls",
    "topics",
    "crawl_difficulty",
    "search_hints",
    "fallback_search_queries",
    "notes",
}


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    data = yaml.safe_load(SOURCES.read_text(encoding="utf-8"))
    sources = data.get("sources", []) if isinstance(data, dict) else []
    if not sources:
        print("No sources found", file=sys.stderr)
        return 1

    ids: set[str] = set()
    errors: list[str] = []

    for index, source in enumerate(sources, start=1):
        sid = source.get("id", f"<missing:{index}>")
        missing = sorted(REQUIRED - set(source))
        if missing:
            errors.append(f"{sid}: missing fields: {', '.join(missing)}")
        if sid in ids:
            errors.append(f"{sid}: duplicate id")
        ids.add(sid)
        if not is_url(str(source.get("base_url", ""))):
            errors.append(f"{sid}: invalid base_url")
        for url in source.get("entry_urls", []) or []:
            if not is_url(str(url)):
                errors.append(f"{sid}: invalid entry_url: {url}")
        for list_field in ("entry_urls", "topics", "search_hints", "fallback_search_queries"):
            value = source.get(list_field)
            if not isinstance(value, list) or not value:
                errors.append(f"{sid}: {list_field} must be a non-empty list")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(sources)} sources from {SOURCES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
