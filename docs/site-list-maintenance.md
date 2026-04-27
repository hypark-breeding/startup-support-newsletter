# Site List Maintenance

## Add a Source

Add one entry to `data/sources.yaml` with:

- stable `id`
- official `name` and `name_ko`
- `region`
- `organization_type`
- `source_priority`
- `coverage_priority`
- `base_url`
- one or more `entry_urls`
- `topics`
- `crawl_difficulty`
- `search_hints`
- `fallback_search_queries`
- `notes`

Then run:

```bash
python3 scripts/validate_sources.py
```

## Review Cadence

- High-priority Seoul-wide sources: monthly
- District and sector sources: quarterly
- Low-confidence sources: verify before each use

## Promotion Rule

Promote a source to `high` coverage only if it repeatedly publishes startup support
programs or acts as an official application surface.
