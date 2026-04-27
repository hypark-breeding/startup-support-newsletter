# Startup Support Newsletter

Agent-friendly project for collecting Korean government startup support announcements,
starting with Seoul-area sources.

The goal is to answer questions like:

- "서울 창업지원 정보 알려줘"
- "마포구 예비창업자가 신청할 수 있는 지원사업 모아줘"
- "이번 주 서울권 창업지원사업 뉴스레터 만들어줘"

## Approach

This starts as a Skill-first project, not an MCP-first project.

- `government-startup-support/SKILL.md` tells agents how to search, verify, normalize,
  and summarize startup support announcements.
- `data/sources.yaml` keeps official and high-value source seeds for Seoul.
- `data/regions.yaml` maps Seoul districts and aliases.
- `data/keywords.yaml` captures Korean search terms that announcements commonly use.
- `docs/` explains collection policy and newsletter format.

Add an MCP server later when repeated crawling, change detection, persistent storage, or
scheduled newsletter delivery becomes necessary.

## Quick Checks

```bash
python3 scripts/validate_sources.py
```

## Repository Status

Initial scope is Seoul. The first version intentionally favors source quality and
maintainability over broad national coverage.
