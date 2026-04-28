# Insight Discovery Email Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add source discovery, recurring-program insight, VC insight, designed report rendering, and real email delivery guidance to the startup-support skill.

**Architecture:** Keep the skill agent-facing and add small standard-library scripts for rendering and email delivery. GPT Researcher and Crawl4AI remain external research/extraction tools documented in the skill workflow.

**Tech Stack:** Python 3 standard library, JSON schema, SMTP, SendGrid HTTP API, Mailgun HTTP API, existing skill manifest validation.

---

### Task 1: Renderer Tests

**Files:**
- Create: `tests/test_render_insight_report.py`
- Create later: `scripts/render_insight_report.py`

- [x] **Step 1: Write failing renderer test**

The test imports `scripts/render_insight_report.py`, renders a sample insight report, and asserts the HTML contains sections for current opportunities, recurring opportunities, VC insights, next actions, and escaped HTML.

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_render_insight_report tests.test_send_report_email`
Expected: FAIL because `scripts/render_insight_report.py` is missing.

### Task 2: Email Tests

**Files:**
- Create: `tests/test_send_report_email.py`
- Create later: `scripts/send_report_email.py`

- [x] **Step 1: Write failing email config tests**

The tests cover SMTP provider preference, missing SMTP settings, SendGrid/Mailgun config resolution, and multipart SMTP message creation.

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_render_insight_report tests.test_send_report_email`
Expected: FAIL because `scripts/render_insight_report.py` is missing.

### Task 3: Implement Renderer and Email Script

**Files:**
- Create: `scripts/render_insight_report.py`
- Create: `scripts/send_report_email.py`

- [x] **Step 1: Implement renderer**

Create a standard-library renderer that reads an insight report JSON file and writes a styled HTML report. Escape all user-provided values.

- [x] **Step 2: Implement email delivery script**

Create provider config resolution for SMTP, SendGrid, and Mailgun. Support `.env` loading, dry-run preview, HTML body input, and optional plain-text body.

- [x] **Step 3: Run tests**

Run: `python3 -m unittest tests.test_render_insight_report tests.test_send_report_email`
Expected: PASS.

### Task 4: Skill and Manifest Documentation

**Files:**
- Modify: `skills/government-startup-support/SKILL.md`
- Modify: `government-startup-support/SKILL.md`
- Create: `docs/research-insights.md`
- Create: `docs/email-delivery.md`
- Create: `schemas/insight-report.schema.json`
- Modify: `skill-manifest.json`
- Modify: `scripts/validate_skill_package.py`

- [x] **Step 1: Add discovery and email workflows to the skill**

Add instructions for unknown-source discovery, 12-month recurrence windows, GPT Researcher, Crawl4AI, VC insights, designed report rendering, and real email delivery.

- [x] **Step 2: Update manifest and validation**

Add new docs, schema, and script paths to `skill-manifest.json`; make validation check `script_paths`.

- [x] **Step 3: Run package validation**

Run: `python3 scripts/validate_skill_package.py`
Expected: `Validated skill package: government-startup-support`.

### Task 5: Final Verification

**Files:**
- All changed files

- [x] **Step 1: Run all verification commands**

Run:

```bash
python3 -m unittest tests.test_render_insight_report tests.test_send_report_email
python3 scripts/validate_skill_package.py
python3 scripts/validate_sources.py
git diff --check
```

Expected: all commands exit 0.
