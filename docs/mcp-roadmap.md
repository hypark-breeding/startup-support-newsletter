# MCP Roadmap

Start with Skill + YAML source registry.

Add an MCP server when the project needs:

- scheduled crawling
- persistent database storage
- duplicate detection across weeks
- "new since last week" diffs
- newsletter delivery integrations
- discovery-mode research with GPT Researcher and Crawl4AI
- designed report rendering and email delivery status checks
- procurement API connectors and bid-deadline monitoring
- event and meetup feed monitoring
- source health checks
- API access for other agents

Possible MCP tools:

- `search_sources(region, support_type, stage)`
- `fetch_notice(source_id, url)`
- `list_new_notices(since)`
- `render_newsletter(region, date_range)`
- `discover_sources(region, founder_profile)`
- `research_insights(query, date_range)`
- `send_report_email(report_id, recipients)`
- `list_procurement_opportunities(query, date_range)`
- `list_event_opportunities(region, date_range)`
- `mark_source_health(source_id, status)`
