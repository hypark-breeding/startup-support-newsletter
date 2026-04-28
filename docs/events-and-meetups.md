# Events And Meetups

Use this workflow when the user asks for startup events, founder meetups, demo days,
seminars, webinars, accelerator office hours, networking opportunities, or investor-facing events.

## Source Priority

1. Official public startup portals and program pages.
2. Public institutions, startup hubs, accelerators, VC or ecosystem organizations.
3. High-value community sources as lead sources only.
4. Private event aggregators only as discovery leads unless the event organizer page confirms details.

## Classification

Normalize event-like items as `event_opportunities`.

Recommended fields:

- title
- host
- event_type: `event|meetup|demo_day|webinar|education|conference|office_hours`
- event_date
- registration_deadline
- location
- audience
- cost
- registration_url
- source_url
- confidence

## Workflow

1. Search official event and education pages first.
2. Use Crawl4AI for event pages with JavaScript-heavy listings.
3. Verify date, registration deadline, host, venue, and cost before recommending attendance.
4. Add event dates to calendar events when possible.
5. Explain why the event matters: customer discovery, investor access, partner fit, procurement readiness, or founder learning.

## Output

Keep events separate from grants and procurement. In combined reports, use an `Events and meetups` section and include date-ordered items.
