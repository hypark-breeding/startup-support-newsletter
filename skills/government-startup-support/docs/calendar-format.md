# Calendar Format

Use this format when scraped startup support information should be organized as a
date-based schedule.

## Event Types

- `application_open`: application period starts.
- `application_deadline`: application period ends.
- `event`: competition, demo day, seminar, networking, or program event.
- `briefing`: information session or briefing.
- `interview`: evaluation, interview, or presentation review.
- `result_announcement`: selection result announcement.

## Calendar Event Schema

```json
{
  "type": "application_deadline",
  "title": "Program title",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "timezone": "Asia/Seoul",
  "organization": "Organization name",
  "region": "seoul",
  "districts": [],
  "source_url": "https://official.example.com/notice",
  "apply_url": "https://official.example.com/apply",
  "status": "open|upcoming|closed|unknown",
  "confidence": "high|medium|low",
  "notes": "Keep source-specific date wording or caveats here."
}
```

## Markdown Schedule

Group by date in ascending order.

```markdown
## YYYY-MM-DD

### 마감: Program Title

- Organization:
- Time:
- Target:
- Benefit:
- Official link:
- Confidence:
```

## ICS Mapping

When creating `.ics` calendar content:

- `SUMMARY`: event type label + program title.
- `DESCRIPTION`: benefit, eligibility, official URL, apply URL, contact, confidence.
- `DTSTART`: event date and time if known.
- `DTEND`: same day with a short default duration for non-deadline events.
- `URL`: official source URL.
- `CATEGORIES`: `startup-support`, region, support type, event type.

Do not invent missing times. For all-day deadlines, use an all-day date event unless the
source states a specific time.
