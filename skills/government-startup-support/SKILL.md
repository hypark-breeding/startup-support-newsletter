---
name: government-startup-support
description: Find Korean government and public-sector startup support announcements, discover unknown sources and recurring opportunities, collect VC or investor insights, and produce verified briefings, designed reports, newsletters, or email deliveries.
license: MIT
metadata:
  category: startup
  locale: ko-KR
  phase: v0
---

# Government Startup Support

Use this skill when the user asks for Korean startup support information across Korea, especially nationwide or regional queries such as "전국 창업지원 정보", "부산 AI 스타트업 지원사업", or "URL은 모르는데 이번 주 창업지원사업 뉴스레터".

## What this skill does

It searches official and high-value public-sector sources, normalizes program details,
and produces an answer, calendar-style schedule, or newsletter that helps founders avoid manually visiting many
SEO-unfriendly websites. It can also run discovery-mode research when the user does not know
which sites to check, identify likely recurring programs from the last 12 months, add VC or
accelerator insight, render a designed HTML report, and send the report by email.

Default coverage is nationwide. If the user does not provide URLs, treat that as normal: discover candidate official sources first, then verify and extract them. Do not assume the bundled source list is complete.

## When to use

- The user asks for startup support programs by region.
- The user asks for open or upcoming government support announcements.
- The user asks for a weekly newsletter of startup programs.
- The user asks to organize scraped programs by date, deadline, or calendar schedule.
- The user asks whether a program is worth applying to based on an attached announcement and their business plan.
- The user asks for support programs by stage, district, industry, or founder profile.
- The user says they do not know which startup support sites to check.
- The user asks what truly opened this year or what appeared last year and may recur this year.
- The user asks for insight research, market signals, VC information, accelerators, or TIPS operator context.
- The user asks for a designed report instead of a plain answer.
- The user asks to email the report.
- The user asks for public procurement, bids, RFPs, ordering plans, public purchase, or municipal contract opportunities.
- The user asks for startup events, founder meetups, demo days, seminars, webinars, or networking opportunities.

## When not to use

- Direct application submission.
- Login-only source collection without explicit user approval.
- Legal, tax, or grant eligibility guarantees.
- Uploading, committing, or exposing the user's private business plan without explicit approval.

## Source Priority

1. Official national portals, central ministries, and public institutions.
2. Official city/province, municipal, and affiliated public-organization pages.
3. Regional startup hubs, CCEI pages, technoparks, and sector-specific public hubs.
4. National aggregators such as K-Startup, Bizinfo, SMEs24, KONEPS, and Data.go.kr for discovery and cross-checking.
5. Private aggregators only as lead sources, never as final authority.

## Workflow

### 1. Clarify the request scope

Resolve:

- Region: nationwide by default; city/province, district-specific, or source-specific when provided.
- Founder stage: pre-founder, early startup, scale-up, SME, small business.
- Support type: grant, space, acceleration, mentoring, R&D, PoC, global expansion,
  loan/guarantee, hiring, education, competition, demo day.
- Date basis: use KST and convert relative dates to absolute dates.

Ask at most 1-3 short questions only if the missing input changes the result materially. Do not ask the user for source URLs just to begin; missing URLs should trigger discovery mode.

### 2. Load source seeds

Read:

- `data/sources.yaml`
- `data/regions.yaml`
- `data/keywords.yaml`
- `docs/research-insights.md` when the request involves unknown-source discovery, recurring programs, or VC/investor insight.
- `docs/procurement-opportunities.md` when the request involves bids, RFPs, public purchase, ordering plans, or municipal contracts.
- `docs/events-and-meetups.md` when the request involves events, meetups, demo days, seminars, webinars, or networking.

Select sources matching the region and support type. For nationwide or no-URL queries, start with high-priority national seeds, then use GPT Researcher and Crawl4AI to discover central-government, city/province, municipal, CCEI, technopark, procurement, event, and ecosystem sources. For region-specific queries, add local official sources after the national seeds.

### 3. Search official sources first

Use direct source URLs when the user provides them. If the user does not provide URLs, discover candidate official URLs with `data/sources.yaml`, GPT Researcher, and fallback search queries before extraction. If a site is difficult to navigate, use fallback queries from `sources.yaml`.

Common query patterns:

```text
site:{domain} 창업지원 모집
site:{domain} 스타트업 지원사업 공고
site:{domain} 예비창업 모집 공고
site:{domain} 입주기업 모집 창업
site:{domain} 사업화 지원 스타트업
```

### 4. Normalize each candidate

Capture this schema:

```json
{
  "title": "",
  "organization": "",
  "source_url": "",
  "apply_url": "",
  "region": "national|city_or_province",
  "districts": [],
  "support_types": [],
  "target_stage": [],
  "benefit_summary": "",
  "application_period": {
    "start": "",
    "end": "",
    "status": ""
  },
  "calendar_events": [
    {
      "type": "application_open|application_deadline|event|briefing|interview|result_announcement",
      "title": "",
      "date": "YYYY-MM-DD",
      "time": "",
      "timezone": "Asia/Seoul",
      "source_url": "",
      "notes": ""
    }
  ],
  "eligibility_summary": "",
  "contact": "",
  "verified_at": "YYYY-MM-DD",
  "confidence": "high|medium|low"
}
```

### 5. Analyze attachments when needed

If the official page has attached announcement files, inspect them before making fit or eligibility recommendations.

File type priority:

1. `pdf`
2. `hwpx`
3. `doc` / `docx`

Fallback formats include `hwp`, images, and zip archives. See `docs/attachment-analysis.md` and `docs/document-processing-integrations.md`.

Use available document-processing skills, MCP tools, or local parsers for PDF/HWPX/Word extraction before normalizing the result.

Extract eligibility, exclusions, required documents, evaluation criteria, benefits, obligations, and schedules from the best available attachment. Store local working downloads under `downloads/` and never commit them.

### 6. Compare with the user's business plan when requested

When the user provides or points to a business plan, compare it against the announcement using `docs/business-plan-fit.md`.

Return a recommendation level:

- `strong_apply`
- `apply_with_edits`
- `watch_or_prepare`
- `low_priority`
- `do_not_apply`

Always separate confirmed disqualifiers from fixable gaps. If the plan file is private, keep analysis local and do not commit or quote sensitive sections unnecessarily.

### 7. Build insight reports when requested

For source discovery, recurring-program, VC insight, or designed report requests, normalize
findings into `schemas/insight-report.schema.json`. Render HTML with
`scripts/render_insight_report.py` when the user wants a designed report. Keep generated
reports under `private/` unless the user explicitly asks to commit a sanitized example.

### 8. Build calendar events

For every candidate, create date-based events whenever the source provides dates.

Required event types:

- `application_open`: application period start date.
- `application_deadline`: final application deadline.

Optional event types:

- `event`: orientation, demo day, seminar, or competition date.
- `briefing`: information session or briefing date.
- `interview`: evaluation/interview/presentation date.
- `result_announcement`: expected selection result date.

Rules:

- Use `Asia/Seoul` as the timezone.
- Convert relative dates to absolute `YYYY-MM-DD` dates.
- Preserve exact source wording in `notes` when dates are ambiguous.
- If only a deadline is known, still create an `application_deadline` event.
- If time is missing, leave `time` empty instead of inventing it.
- Sort events by date ascending.
- Use `docs/calendar-format.md` for calendar-style output.

### 9. Filter and rank

Prioritize:

- Currently open applications.
- Officially verified source URLs.
- Strong fit to the user's location, industry, or founder stage.
- Higher-value benefits such as cash grants, office space, PoC, R&D, acceleration,
  global expansion, or loan guarantees.
- Imminent deadlines.

### 10. Produce the answer

For a short nationwide or regional answer, provide:

- Open programs.
- Upcoming or recurring sources to watch.
- Why each item fits.
- Official links.
- Verification date.

For a fit analysis, use `docs/business-plan-fit.md` and include evidence from the official attachment.

For a calendar-style schedule, use `docs/calendar-format.md`.

For an insight report, use `docs/research-insights.md` and include:

- Open now.
- New this year.
- Procurement opportunities.
- Events and meetups.
- Likely recurring.
- Discovered sources.
- VC insights.
- Next actions.

For a newsletter, use `docs/newsletter-format.md` and include the calendar section when relevant.

### 11. Email the designed report when requested

Use `docs/email-delivery.md` and `scripts/send_report_email.py`.

If email configuration is missing, ask the user for the missing provider settings. Support
SMTP, SendGrid, and Mailgun. Do not commit secrets or generated private reports.

Run a dry-run preview before real delivery when working in a new environment:

```bash
python3 scripts/send_report_email.py --to user@example.com --subject "?? ???? ???? ???" --html-file private/insight-report.html --dry-run
```

## Failure Modes

- If official source pages are JavaScript-heavy, use site search and public search
  fallback queries, then cross-check the final result on the official page.
- If only a private aggregator has the result, mark it as a lead and do not treat it as
  verified.
- If a deadline is missing, say so clearly and include the official contact or source.
- If a region-specific request has sparse results, expand to nationwide sources and clearly label the expansion.

## Done When

- The answer includes official links where possible.
- Dates are absolute and KST-aware.
- Date-based programs are also represented as calendar events when possible.
- Attachment-based fit analysis uses the priority `pdf > hwpx > word`.
- Discovery reports separate current opportunities from recurring candidates, procurement, events, meetups, and VC/investor signals.
- Each recommendation has a source and a confidence level.
- Requested designed reports can be rendered to HTML and sent by configured email provider.
- Stale, closed, or uncertain items are labeled.
