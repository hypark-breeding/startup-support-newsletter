# Startup Support Newsletter

Agent-friendly project for collecting Korean government startup support announcements, starting with Seoul-area sources.

The goal is to answer questions like:

- "서울 창업지원 정보 알려줘"
- "마포구 예비창업자가 신청할 수 있는 지원사업 모아줘"
- "이번 주 서울권 창업지원사업 뉴스레터 만들어줘"

## Approach

This starts as a Skill-first project, not an MCP-first project.

- `skills/government-startup-support/SKILL.md` tells agents how to search, verify, normalize, and summarize startup support announcements.
- `skill-manifest.json` describes the installable skill package for coding agents.
- `scripts/install_skill.sh` installs the skill into common home-directory agent skill locations.
- `data/sources.yaml` keeps official and high-value source seeds for Seoul.
- `data/regions.yaml` maps Seoul districts and aliases.
- `data/keywords.yaml` captures Korean search terms that announcements commonly use.
- `docs/` explains collection policy, attachment analysis, calendar output, and newsletter format.
- `calendar-view/` provides a static calendar UI for normalized collected events.

Add an MCP server later when repeated crawling, change detection, persistent storage, or scheduled newsletter delivery becomes necessary.

## Attachment and Fit Analysis

When an official announcement includes attachments, agents should inspect them before judging fit. File type priority is `pdf > hwpx > word`. User business plans and downloaded attachments should stay local and must not be committed.

## Quick Checks

```bash
python3 scripts/validate_sources.py
python3 scripts/validate_skill_package.py
```

## Install As A Skill

For agents that support home-directory skills:

```bash
git clone https://github.com/Malko-potatos/startup-support-newsletter.git
cd startup-support-newsletter
bash scripts/install_skill.sh
```

The installer copies `skills/government-startup-support` into:

- `~/.agents/skills/government-startup-support`
- `~/.codex/skills/government-startup-support` when `~/.codex/skills` exists
- `~/.claude/skills/government-startup-support` when `~/.claude/skills` exists

Agents can also read `skill-manifest.json` and copy the `skill_path` manually.

## Repository Status

Initial scope is Seoul. The first version intentionally favors source quality and maintainability over broad national coverage.
