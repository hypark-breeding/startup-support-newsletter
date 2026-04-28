# Collection Workflow

## Nationwide Or Regional Query

1. Resolve region aliases from `data/regions.yaml`; if the user gives no region, use `national`.
2. If the user provides no URL, start from high-priority national seeds and discovery mode instead of asking for a URL.
3. Search national official seeds first: K-Startup, Bizinfo, SMEs24, CCEI, KONEPS, Data.go.kr, and high-value ecosystem event sources.
4. Add city/province, municipal, CCEI, technopark, local public agency, and sector hub sources discovered by GPT Researcher or source fallback queries.
5. Search direct entry URLs when known.
6. Use fallback search queries if navigation or JavaScript blocks discovery.
7. Normalize candidates into the schema described in the skill entrypoint `SKILL.md`
   for the current package.
8. Extract application dates, deadlines, briefings, interviews, result dates, bid deadlines, registration deadlines, and event dates into calendar events.
9. Deduplicate by title, organization, deadline, and application URL.
10. Rank open official programs first.
11. Sort calendar events by date ascending.

## Nationwide Source Strategy

Start with national discovery seeds:

- K-Startup national startup support portal
- Bizinfo national support-program aggregator
- SMEs24 policy notices
- Creative Economy Innovation Centers integrated site
- KONEPS and Data.go.kr procurement sources
- Startup Alliance and official startup event portals for ecosystem signals

Then add regional sources:

- City/province and municipal startup or economic-promotion pages
- Regional CCEI pages
- Regional technoparks
- Local contract/procurement portals
- Sector hubs such as AI, bio, manufacturing, content, or climate clusters

Seoul sources remain high-quality regional seeds, not the default scope.

## Procurement And Event Query

1. Resolve whether the user wants startup support, procurement, events, or a combined report.
2. For procurement, search `data-go-kr-g2b-bid-api`, `g2b-bid-notices`, and discovered municipal contract portals first.
3. Ask for `DATA_GO_KR_SERVICE_KEY` before live KONEPS API calls when it is missing.
4. For events and meetups, search official startup portals and high-value ecosystem sources first.
5. Normalize procurement into `schemas/procurement-opportunity.schema.json` and events into `schemas/event-opportunity.schema.json`.
6. Keep procurement, events, startup support, recurring programs, and VC insights in separate report sections.
7. Add bid deadlines, registration deadlines, and event dates to calendar events when available.
