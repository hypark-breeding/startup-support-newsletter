#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="government-startup-support"
SOURCE="${ROOT}/skills/${SKILL_NAME}"
HWPX_SKILL_NAME="hwpxskill"
HWPX_REPO_URL="${HWPX_REPO_URL:-https://github.com/Canine89/hwpxskill.git}"
HWPX_CACHE="${ROOT}/.cache/${HWPX_SKILL_NAME}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
PIP_INSTALL_ARGS="${PIP_INSTALL_ARGS:---user}"
REQUIRED_PYTHON_PACKAGES=("gpt-researcher" "crawl4ai")
BUILD_INSTALLABLE_SCRIPT="${ROOT}/scripts/build_installable_skill.sh"

if [ ! -x "${BUILD_INSTALLABLE_SCRIPT}" ]; then
  echo "Missing installable skill builder: ${BUILD_INSTALLABLE_SCRIPT}" >&2
  exit 1
fi
"${BUILD_INSTALLABLE_SCRIPT}"

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
  printf 'Installed %s -> %s
' "${label}" "${target}"
}

install_required_python_tools() {
  if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    echo "Missing required Python executable: ${PYTHON_BIN}" >&2
    exit 1
  fi

  if ! "${PYTHON_BIN}" -m pip --version >/dev/null 2>&1; then
    echo "Missing pip for ${PYTHON_BIN}. Install pip before running this installer." >&2
    exit 1
  fi

  local pip_args=()
  if [ -n "${PIP_INSTALL_ARGS}" ]; then
    read -r -a pip_args <<< "${PIP_INSTALL_ARGS}"
  fi

  "${PYTHON_BIN}" -m pip install "${pip_args[@]}" "${REQUIRED_PYTHON_PACKAGES[@]}"

  local user_base
  user_base="$(${PYTHON_BIN} -m site --user-base 2>/dev/null || true)"
  if [ -n "${user_base}" ]; then
    export PATH="${user_base}/bin:${PATH}"
  fi

  if ! command -v crawl4ai-setup >/dev/null 2>&1; then
    echo "Missing crawl4ai-setup after installing crawl4ai. Ensure the Python user bin directory is on PATH." >&2
    exit 1
  fi

  crawl4ai-setup

  "${PYTHON_BIN}" - <<'PY'
import importlib.util
import sys

required = {
    "gpt-researcher": "gpt_researcher",
    "crawl4ai": "crawl4ai",
}
missing = [name for name, module in required.items() if importlib.util.find_spec(module) is None]
if missing:
    print("Missing required Python packages after install: " + ", ".join(missing), file=sys.stderr)
    raise SystemExit(1)
PY

  printf 'Installed required research tools: %s
' "${REQUIRED_PYTHON_PACKAGES[*]}"
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

install_required_python_tools
install_main_skill
fetch_hwpxskill
install_hwpxskill

printf 'Done. Agents can now load %s with companion skill %s and required research tools.
' "${SKILL_NAME}" "${HWPX_SKILL_NAME}"