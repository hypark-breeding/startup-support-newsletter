# Install

This repository is structured so coding agents can install
`government-startup-support` as a home-directory skill.

## Automatic Install

```bash
git clone https://github.com/Malko-potatos/startup-support-newsletter.git
cd startup-support-newsletter
bash scripts/install_skill.sh
```

The installer also installs mandatory Python research tools before copying skills:

- `gpt-researcher`
- `crawl4ai`

It runs `crawl4ai-setup` after package installation. If either package or the Crawl4AI setup step fails, the installer exits non-zero and the skill install is incomplete. Set `PYTHON_BIN` to choose the Python executable and `PIP_INSTALL_ARGS` to override the default `--user` pip install argument.

The installer always writes to:

```text
~/.agents/skills/government-startup-support
```

It also writes to these locations when the parent skill directory already exists:

```text
~/.codex/skills/government-startup-support
~/.claude/skills/government-startup-support
```

## Manual Install

Copy this directory:

```text
skills/government-startup-support
```

Into one of these locations:

```text
~/.agents/skills/government-startup-support
~/.codex/skills/government-startup-support
~/.claude/skills/government-startup-support
```

## Agent Discovery

Agents should read:

```text
skill-manifest.json
```

Then install `skill_path` and load `entrypoint`.

## GitHub Path Install (skill-installer)

When installing from GitHub path, use the self-contained skill folder path:

```text
https://github.com/Malko-potatos/startup-support-newsletter/tree/main/skills/government-startup-support
```

Equivalent repo/path form:

```text
--repo Malko-potatos/startup-support-newsletter --path skills/government-startup-support
```

This path includes `SKILL.md` and the bundled `docs`, `data`, `schemas`, and `scripts` directories so references in the skill remain resolvable after installation.
