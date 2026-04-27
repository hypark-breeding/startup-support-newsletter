# Collection Workflow

## Regional Query

1. Resolve region aliases from `data/regions.yaml`.
2. Select `high` coverage sources for Seoul-wide queries.
3. Add district or cluster sources when the query names a district.
4. Search direct entry URLs first.
5. Use fallback search queries if navigation or JavaScript blocks discovery.
6. Normalize candidates into the schema in `government-startup-support/SKILL.md`.
7. Extract application dates, deadlines, briefings, interviews, result dates, and event dates into calendar events.
8. Deduplicate by title, organization, deadline, and application URL.
9. Rank open official programs first.
10. Sort calendar events by date ascending.

## Seoul Initial Source Strategy

Start with:

- Startup Plus
- Seoul Business Agency
- Seoul CCEI
- Seoul Campus Town
- Bizinfo Seoul-filtered results
- K-Startup Seoul-filtered results

Then add:

- Gwanak S Valley for Gwanak-specific requests
- Seoul AI Hub for AI/Yangjae requests
- Seoul Bio Hub for bio/healthcare/Hongneung requests
- Seoul 50 Plus Foundation for middle-aged founder/employer support requests
