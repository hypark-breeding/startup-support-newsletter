# MCP Roadmap

Start with Skill + YAML source registry.

Add an MCP server when the project needs:

- scheduled crawling
- persistent database storage
- duplicate detection across weeks
- "new since last week" diffs
- newsletter delivery integrations
- source health checks
- API access for other agents

Possible MCP tools:

- `search_sources(region, support_type, stage)`
- `fetch_notice(source_id, url)`
- `list_new_notices(since)`
- `render_newsletter(region, date_range)`
- `mark_source_health(source_id, status)`
