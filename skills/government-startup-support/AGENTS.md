# Repository Instructions

This repository builds an agent-friendly workflow for finding Korean government
startup support programs, procurement notices, events, and investor-adjacent insights, then turning them into nationwide or regional briefings, designed reports, newsletters, or email deliveries.

## Core Principles

- User-facing replies should be Korean by default.
- Agent-facing instructions, durable docs, templates, and automation should be English
  whenever practical.
- Treat WSL as the development engine and Windows as the control plane.
- Prefer official sources first, then cross-check with aggregators.
- Startup support deadlines and eligibility change often. Always perform fresh source
  checks before giving final recommendations.

## Scope

- Default coverage: nationwide Korea. Users may provide no URLs; discovery mode should find official source candidates first.
- Primary installable skill: `skills/government-startup-support/SKILL.md`.
- Compatibility skill path: `government-startup-support/SKILL.md`.
- Source registry: `data/sources.yaml`.
- Regional aliases: `data/regions.yaml`.
- Search vocabulary: `data/keywords.yaml`.

## Safety

- Do not submit applications or create accounts for users.
- Do not scrape behind logins unless the user explicitly provides access and approves.
- Never commit secrets, API keys, browser cookies, or private application data.
- Mark stale or uncertain information clearly instead of presenting it as current.

## Verification

- Run `python3 scripts/validate_sources.py` after changing `data/sources.yaml`.
- Run `python3 scripts/validate_skill_package.py` after changing install layout.
- For user-facing answers, cite official source URLs whenever possible.
