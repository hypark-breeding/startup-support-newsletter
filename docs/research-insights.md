# Research Insights

Use this workflow when the user does not know which startup-support sites to check, or when they ask for broader insight beyond a known source list.

## Goal

Move from known-source lookup to nationwide opportunity discovery:

- Find programs that are open or announced this year across Korea.
- Identify programs seen in the last 12 months that may recur this year.
- Discover official or high-value source sites the user did not know.
- Add investor, VC, accelerator, TIPS operator, procurement, event, and market signals when relevant.

No user-provided URL is required. If the user has no URLs, use the bundled source seeds only as a starting point and discover additional official sources before verification.

## Time Window

Default window: the last 12 months from the user's current KST date.
Default scope: nationwide Korea unless the user narrows the region.

Use these buckets:

- `open_now`: current year announcements with official source confirmation.
- `new_this_year`: current year announcements that are not necessarily open today.
- `likely_recurring`: last-year or last-12-month announcements likely to repeat.
- `watchlist`: institutions, portals, or programs to check again near the expected window.
- `vc_insights`: investor or accelerator signals relevant to the founder profile.
- `procurement_opportunities`: public bids, RFPs, public purchase, and municipal contract opportunities.
- `event_opportunities`: startup events, meetups, seminars, demo days, and networking opportunities.

Never present last-year data as currently open. Label it as a recurrence candidate.

## Required Installation

`gpt-researcher` and `crawl4ai` are mandatory dependencies for discovery-mode research. The installer must install both packages and run `crawl4ai-setup`. If either dependency is unavailable, do not present discovery-mode insight research as supported; report the missing installation step instead.

## Tool Roles

### GPT Researcher

Use GPT Researcher for broad discovery and synthesis:

- Generate research questions from the founder profile, nationwide or regional scope, industry, and support type.
- Search beyond known source seeds and assume the source list is incomplete.
- Discover national portals, central ministries, city/province sources, municipal sources, CCEI pages, technoparks, procurement portals, events, VC/accelerator signals, and related news.
- Collect candidate source URLs, summaries, source lists, costs, and research context.
- Ask for official-source verification before final recommendations.

Good query shape:

```text
Find Korean startup support programs, procurement notices, startup events, and VC/accelerator signals from the last 12 months for the founder profile. Cover nationwide sources first, then relevant city/province and municipal sources. Separate currently open opportunities from recurring candidates and verify official URLs.
```

### Crawl4AI

Use Crawl4AI to inspect candidate pages:

- Convert JavaScript-heavy pages into clean markdown.
- Extract links, media, and attachment candidates.
- Inspect institutional notice lists and detail pages.
- Preserve source URL and crawl timestamp.

For official notices, use Crawl4AI output as extraction evidence, then normalize into the announcement or insight schema.

## Discovery Workflow

1. Clarify the founder profile only when it materially changes the search.
2. Set the default date range to the last 12 months in KST.
3. Set the default region to nationwide Korea when the user does not specify a region.
4. Start with existing `data/sources.yaml`, but do not assume it is complete.
5. Use GPT Researcher to discover official portals, institution pages, annual programs, procurement sources, events, VC/accelerator signals, and related news.
6. Use Crawl4AI on candidate official pages to extract markdown, links, attachments, and notice metadata.
7. Classify each candidate into `open_now`, `new_this_year`, `likely_recurring`, `watchlist`, `procurement_opportunities`, `event_opportunities`, or `vc_insights`.
8. Verify current opportunities against official URLs or attached notices.
9. Keep private drafts and downloaded files under `private/` or `downloads/` and do not commit them.
10. Render the final insight report with `scripts/render_insight_report.py` when a designed HTML report is requested.

## Confidence Rules

- `high`: official source page or official attachment confirms the item.
- `medium`: reliable institution, press release, or repeated historical pattern supports the item, but it is not confirmed as currently open.
- `low`: lead source, private aggregator, or incomplete source chain.

## VC and Investor Insight Rules

Treat VC content as context, not financial advice.

Capture:

- Investor or accelerator name.
- Thesis or signal.
- Stage and sector fit.
- Portfolio or program connection when public.
- Source URL and verification date.

Use labels:

- `fundraising_signal`: evidence of investor interest or activity.
- `partner_fit`: likely mentor, accelerator, or strategic partner.
- `watchlist`: useful source to monitor.

Avoid claiming that an investor will fund the user.

## Output Shape

Normalize designed reports into `schemas/insight-report.schema.json`.

Minimum useful sections:

- Executive summary.
- Open now.
- New this year.
- Procurement opportunities.
- Events and meetups.
- Likely recurring.
- Discovered sources.
- VC insights.
- Next actions.
- Sources and verification date.

## Done When

- Current opportunities and recurrence candidates are separated.
- Every current opportunity has an official or clearly labeled source.
- Last-year items include last seen period and expected watch window.
- The search covers nationwide seeds when the user gives no URL or no region.
- VC/investor items are labeled as signals, not guarantees.
- The report can be rendered to HTML and optionally sent by email.
