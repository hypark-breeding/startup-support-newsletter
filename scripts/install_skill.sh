#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="government-startup-support"
SOURCE="${ROOT}/skills/${SKILL_NAME}"

if [ ! -f "${SOURCE}/SKILL.md" ]; then
  echo "Missing skill source: ${SOURCE}/SKILL.md" >&2
  exit 1
fi

copy_skill() {
  local target="$1"
  mkdir -p "$(dirname "${target}")"
  rm -rf "${target}"
  mkdir -p "${target}"
  cp -R "${SOURCE}/." "${target}/"
  printf 'Installed %s -> %s\n' "${SKILL_NAME}" "${target}"
}

copy_skill "${HOME}/.agents/skills/${SKILL_NAME}"

if [ -d "${HOME}/.codex/skills" ]; then
  copy_skill "${HOME}/.codex/skills/${SKILL_NAME}"
fi

if [ -d "${HOME}/.claude/skills" ]; then
  copy_skill "${HOME}/.claude/skills/${SKILL_NAME}"
fi

printf 'Done. Agents can now load %s from home skill directories.\n' "${SKILL_NAME}"
