# Calendar View

A dependency-free static calendar view for normalized startup support events.

## Input

Load JSON shaped like `examples/calendar-events.json`, either as a raw array or as:

```json
{
  "calendar_events": []
}
```

Each event should follow `docs/calendar-format.md`.

## Open Locally

From the repository root:

```bash
python3 -m http.server 4173
```

Then open:

```text
http://localhost:4173/calendar-view/
```

The page includes sample events and a JSON file picker for collected event data.
