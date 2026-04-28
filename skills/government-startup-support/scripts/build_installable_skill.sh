#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_SKILL_DIR="${ROOT}/skills/government-startup-support"
SOURCE_SKILL_MD="${ROOT}/government-startup-support/SKILL.md"

if [ -f "${ROOT}/SKILL.md" ] && [ -d "${ROOT}/data" ] && [ -d "${ROOT}/docs" ] && [ -d "${ROOT}/schemas" ] && [ -d "${ROOT}/scripts" ]; then
  echo "Skill package is already self-contained: ${ROOT}"
  exit 0
fi

if [ ! -f "${SOURCE_SKILL_MD}" ]; then
  echo "Missing source SKILL.md: ${SOURCE_SKILL_MD}" >&2
  exit 1
fi

mkdir -p "${TARGET_SKILL_DIR}"
cp "${SOURCE_SKILL_MD}" "${TARGET_SKILL_DIR}/SKILL.md"

# Keep the installable skill self-contained so GitHub path installers copy all resources.
for dir_name in data docs schemas scripts; do
  rm -rf "${TARGET_SKILL_DIR}/${dir_name}"
  cp -R "${ROOT}/${dir_name}" "${TARGET_SKILL_DIR}/${dir_name}"
done

for file_name in AGENTS.md README.md README.en.md README.ko.md skill-manifest.json .gitignore; do
  if [ -f "${ROOT}/${file_name}" ]; then
    cp "${ROOT}/${file_name}" "${TARGET_SKILL_DIR}/${file_name}"
  fi
done

echo "Built installable skill directory: ${TARGET_SKILL_DIR}"
