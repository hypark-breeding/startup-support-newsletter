#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="government-startup-support"
SOURCE="${ROOT}/skills/${SKILL_NAME}"
HWPX_SKILL_NAME="hwpxskill"
HWPX_REPO_URL="${HWPX_REPO_URL:-https://github.com/Canine89/hwpxskill.git}"
HWPX_CACHE="${ROOT}/.cache/${HWPX_SKILL_NAME}"

if [ ! -f "${SOURCE}/SKILL.md" ]; then
  echo "Missing skill source: ${SOURCE}/SKILL.md" >&2
  exit 1
fi

copy_dir() {
  local source="$1"
  local target="$2"
  local label="$3"
  mkdir -p "$(dirname "${target}")"
  rm -rf "${target}"
  mkdir -p "${target}"
  cp -R "${source}/." "${target}/"
  printf 'Installed %s -> %s\n' "${label}" "${target}"
}

install_main_skill() {
  copy_dir "${SOURCE}" "${HOME}/.agents/skills/${SKILL_NAME}" "${SKILL_NAME}"

  if [ -d "${HOME}/.codex/skills" ]; then
    copy_dir "${SOURCE}" "${HOME}/.codex/skills/${SKILL_NAME}" "${SKILL_NAME}"
  fi

  if [ -d "${HOME}/.claude/skills" ]; then
    copy_dir "${SOURCE}" "${HOME}/.claude/skills/${SKILL_NAME}" "${SKILL_NAME}"
  fi
}

fetch_hwpxskill() {
  mkdir -p "$(dirname "${HWPX_CACHE}")"
  if [ -d "${HWPX_CACHE}/.git" ]; then
    git -C "${HWPX_CACHE}" fetch --depth 1 origin
    git -C "${HWPX_CACHE}" reset --hard origin/HEAD
  else
    rm -rf "${HWPX_CACHE}"
    git clone --depth 1 "${HWPX_REPO_URL}" "${HWPX_CACHE}"
  fi
}

install_hwpxskill() {
  if [ ! -f "${HWPX_CACHE}/SKILL.md" ]; then
    echo "Missing companion skill after clone: ${HWPX_CACHE}/SKILL.md" >&2
    exit 1
  fi

  copy_dir "${HWPX_CACHE}" "${HOME}/.agents/skills/${HWPX_SKILL_NAME}" "${HWPX_SKILL_NAME}"

  if [ -d "${HOME}/.codex/skills" ]; then
    copy_dir "${HWPX_CACHE}" "${HOME}/.codex/skills/${HWPX_SKILL_NAME}" "${HWPX_SKILL_NAME}"
  fi

  if [ -d "${HOME}/.claude/skills" ]; then
    copy_dir "${HWPX_CACHE}" "${HOME}/.claude/skills/${HWPX_SKILL_NAME}" "${HWPX_SKILL_NAME}"
  fi
}

install_main_skill
fetch_hwpxskill
install_hwpxskill

printf 'Done. Agents can now load %s with companion skill %s.\n' "${SKILL_NAME}" "${HWPX_SKILL_NAME}"
