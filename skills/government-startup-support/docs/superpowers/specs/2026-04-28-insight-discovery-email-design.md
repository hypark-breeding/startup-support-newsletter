# Insight Discovery and Email Delivery Design

## Context

The first version assumes the agent knows the important source sites. User feedback shows
the opposite problem: founders often do not know where startup support announcements live.
The skill must discover sources, current announcements, likely recurring programs, and
investment signals without requiring the user to name a portal first.

## Goals

- Discover current-year Korean startup-support announcements from official sources.
- Use a default 12-month evidence window to find programs that may recur this year.
- Clearly separate currently open items from recurrence candidates.
- Use GPT Researcher for broad discovery and synthesis.
- Use Crawl4AI for page extraction, markdown conversion, links, and attachment discovery.
- Include VC, accelerator, TIPS operator, and investment signals as context.
- Render a designed HTML report.
- Send the report by SMTP, SendGrid, or Mailgun when configuration is present.
- Ask the user for missing mail settings when configuration is absent.

## Non-goals

- Do not create accounts, submit applications, or apply on behalf of the user.
- Do not treat last-year announcements as currently open.
- Do not make financial or investment advice claims.
- Do not commit secrets, private reports, business plans, or recipient lists.

## Workflow

1. Resolve user intent: regional support, recurring opportunities, investor insight, or a combined report.
2. Default the research window to the last 12 months in KST.
3. Use existing source seeds, then discover beyond them with GPT Researcher.
4. Crawl and extract candidate pages with Crawl4AI when page structure or JavaScript makes manual extraction unreliable.
5. Classify findings into open now, new this year, likely recurring, watchlist, discovered sources, and VC insights.
6. Normalize findings into `schemas/insight-report.schema.json`.
7. Render the designed report with `scripts/render_insight_report.py`.
8. Preview the email with `scripts/send_report_email.py --dry-run`.
9. Send only after recipient, subject, sender, and provider settings are available.

## Data Model

The insight report schema contains:

- `title`, `region`, `date_range`, `generated_at`, and `summary`.
- `open_now` for confirmed current opportunities.
- `new_this_year` for announced but not necessarily open items.
- `likely_recurring` for historical programs expected to reappear.
- `discovered_sources` for candidate portals or institution pages.
- `vc_insights` for investor and accelerator signals.
- `next_actions` for founder-facing steps.
- `sources` for evidence URLs.

## Email Delivery

The script supports three providers:

- SMTP via `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, and `SMTP_FROM`.
- SendGrid via `SENDGRID_API_KEY` and `SENDGRID_FROM` or `EMAIL_FROM`.
- Mailgun via `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, and `MAILGUN_FROM` or `EMAIL_FROM`.

If settings are missing, the skill asks the user for only the missing values and stores
them outside Git as shell env or a local `.env` file.

## Error Handling

- Missing provider settings produce a clear list of required environment variables.
- Current opportunities without official sources are downgraded to leads.
- Recurring opportunities must include a last seen period and an expected watch window.
- Provider API errors report status and response body without exposing secrets.

## Testing

- Unit tests cover report rendering, HTML escaping, provider selection, missing config,
  and multipart SMTP message generation.
- Package validation checks new docs, schema, and script manifest entries.
- Source validation remains unchanged.
