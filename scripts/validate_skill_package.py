#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install with: python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "skill-manifest.json"


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    skill_path = ROOT / manifest["skill_path"]
    entrypoint = ROOT / manifest["entrypoint"]

    if not skill_path.is_dir():
        return fail(f"Missing skill directory: {skill_path}")
    if not entrypoint.is_file():
        return fail(f"Missing skill entrypoint: {entrypoint}")

    text = entrypoint.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return fail("SKILL.md must start with YAML frontmatter")

    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        return fail("SKILL.md frontmatter is not closed")

    meta = yaml.safe_load(frontmatter)
    if meta.get("name") != manifest["name"]:
        return fail("Manifest name must match SKILL.md frontmatter name")
    if not meta.get("description"):
        return fail("SKILL.md description is required")

    for rel_path in manifest.get("data_paths", []):
        if not (ROOT / rel_path).is_file():
            return fail(f"Missing manifest data path: {rel_path}")

    print(f"Validated skill package: {manifest['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
