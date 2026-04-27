---
name: government-startup-support
description: Find Korean government and public-sector startup support announcements, with Seoul as the initial coverage area, and produce verified regional briefings or newsletters.
license: MIT
metadata:
  category: startup
  locale: ko-KR
  phase: v0
---

# Government Startup Support

Use this skill when the user asks for Korean startup support information, especially
regional queries such as "서울 창업지원 정보", "마포구 예비창업 지원사업", or "이번 주 서울권 창업지원사업 뉴스레터".

## What this skill does

It searches official and high-value public-sector sources, normalizes program details,
and produces an answer, calendar-style schedule, or newsletter that helps founders avoid manually visiting many
SEO-unfriendly websites.

Initial coverage is Seoul.

## When to use

- The user asks for startup support programs by region.
- The user asks for open or upcoming government support announcements.
- The user asks for a weekly newsletter of startup programs.
- The user asks to organize scraped programs by date, deadline, or calendar schedule.
- The user asks for support programs by stage, district, industry, or founder profile.

## When not to use

- Direct application submission.
- Login-only source collection without explicit user approval.
- Legal, tax, or grant eligibility guarantees.

## Source Priority

1. Official program portals and public institutions.
2. Seoul city, district, and affiliated organization pages.
3. Seoul startup hubs and sector-specific public hubs.
4. National aggregators for cross-checking.
5. Private aggregators only as lead sources, never as final authority.

## Workflow

### 1. Clarify the request scope

Resolve:

- Region: Seoul-wide, district-specific, or source-specific.
- Founder stage: pre-founder, early startup, scale-up, SME, small business.
- Support type: grant, space, acceleration, mentoring, R&D, PoC, global expansion,
  loan/guarantee, hiring, education, competition, demo day.
- Date basis: use KST and convert relative dates to absolute dates.

Ask at most 1-3 short questions only if the missing input changes the result materially.

### 2. Load source seeds

Read:

- `data/sources.yaml`
- `data/regions.yaml`
- `data/keywords.yaml`

Select sources matching the region and support type. For Seoul-wide queries, start with
high-priority Seoul-wide sources and then add district or sector sources.

### 3. Search official sources first

Use direct source URLs first. If a site is difficult to navigate, use fallback queries
from `sources.yaml`.

Common query patterns:

```text
site:{domain} 창업지원 모집 서울
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
  "region": "seoul",
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

### 5. Build calendar events

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

### 6. Filter and rank

Prioritize:

- Currently open applications.
- Officially verified source URLs.
- Strong fit to user's district, industry, or founder stage.
- Higher-value benefits such as cash grants, office space, PoC, R&D, acceleration,
  global expansion, or loan guarantees.
- Imminent deadlines.

### 7. Produce the answer

For a short regional answer, provide:

- Open programs.
- Upcoming or recurring sources to watch.
- Why each item fits.
- Official links.
- Verification date.

For a calendar-style schedule, use `docs/calendar-format.md`.

For a newsletter, use `docs/newsletter-format.md` and include the calendar section when relevant.

## Failure Modes

- If official source pages are JavaScript-heavy, use site search and public search
  fallback queries, then cross-check the final result on the official page.
- If only a private aggregator has the result, mark it as a lead and do not treat it as
  verified.
- If a deadline is missing, say so clearly and include the official contact or source.
- If a region-specific request has sparse results, expand to Seoul-wide sources and label
  the expansion.

## Done When

- The answer includes official links where possible.
- Dates are absolute and KST-aware.
- Date-based programs are also represented as calendar events when possible.
- Each recommendation has a source and a confidence level.
- Stale, closed, or uncertain items are labeled.
