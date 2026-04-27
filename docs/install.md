# Install

This repository is structured so coding agents can install
`government-startup-support` as a home-directory skill.

## Automatic Install

```bash
git clone https://github.com/Malko-potatos/startup-support-newsletter.git
cd startup-support-newsletter
bash scripts/install_skill.sh
```

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
