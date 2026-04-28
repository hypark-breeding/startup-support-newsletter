# Startup Support Newsletter

Agent-friendly project for collecting nationwide Korean government startup support announcements, procurement, events, and investor-adjacent insights even when the user does not provide source URLs.

The goal is to answer questions like:

- "Find nationwide Korean startup support programs that opened this year and recurring programs likely to return"
- "Find support programs, procurement notices, and events for a Busan/Gyeongnam AI startup"
- "I do not know the URLs; create this week's startup-support newsletter"

## Approach

This starts as a Skill-first project, not an MCP-first project.

- `skills/government-startup-support/SKILL.md` tells agents how to search, verify, normalize, and summarize startup support announcements.
- `skill-manifest.json` describes the installable skill package for coding agents.
- `scripts/install_skill.sh` installs the skill into common home-directory agent skill locations.
- `data/sources.yaml` keeps national official seeds plus regional expansion candidates.
- `data/regions.yaml` maps nationwide, city/province, and Seoul district aliases.
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

The installer copies `skills/government-startup-support`, installs `Canine89/hwpxskill` for HWPX attachment handling, and installs the mandatory Python packages `gpt-researcher` and `crawl4ai`. It also runs `crawl4ai-setup`; if any required research tool fails to install, the skill install is incomplete. Skill files are copied into:

- `~/.agents/skills/government-startup-support`
- `~/.codex/skills/government-startup-support` when `~/.codex/skills` exists
- `~/.claude/skills/government-startup-support` when `~/.claude/skills` exists

Agents can also read `skill-manifest.json` and copy the `skill_path` manually.

## Repository Status

Current scope is nationwide Korea. Seoul sources remain high-quality regional seeds, while unknown-source requests use GPT Researcher and Crawl4AI discovery mode to expand across national, municipal, and public-institution sources.
