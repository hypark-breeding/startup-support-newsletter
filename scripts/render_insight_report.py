#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Iterable


STYLE = """
:root {
  color-scheme: light;
  --canvas: #f7f4ed;
  --paper: #fffdf7;
  --ink: #15231f;
  --muted: #5e665f;
  --rule: #d7c7a2;
  --urgent: #b33a2f;
  --verified: #1f6f68;
  --info: #2e4e7e;
}
body {
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font-family: "IBM Plex Sans KR", "Noto Sans KR", Arial, sans-serif;
  line-height: 1.6;
}
.page {
  max-width: 920px;
  margin: 0 auto;
  padding: 36px 20px 48px;
}
.masthead {
  border-bottom: 3px solid var(--ink);
  padding-bottom: 18px;
  margin-bottom: 24px;
}
h1, h2, h3 {
  font-family: Fraunces, Georgia, serif;
  letter-spacing: 0;
  line-height: 1.2;
}
h1 {
  font-size: 34px;
  margin: 0 0 12px;
}
h2 {
  font-size: 22px;
  border-bottom: 1px solid var(--rule);
  padding-bottom: 8px;
  margin: 30px 0 14px;
}
h3 {
  font-size: 18px;
  margin: 0 0 8px;
}
.meta, .muted {
  color: var(--muted);
  font-size: 14px;
}
.summary {
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: 18px;
  margin: 18px 0 24px;
}
.grid {
  display: grid;
  gap: 12px;
}
.card {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-left: 5px solid var(--info);
  padding: 16px;
}
.card.open { border-left-color: var(--verified); }
.card.procurement { border-left-color: var(--urgent); }
.card.recurring { border-left-color: var(--urgent); }
.card.event { border-left-color: var(--info); }
.card.vc { border-left-color: var(--info); }
.fields {
  display: grid;
  gap: 4px;
  margin: 0;
}
.fields div {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 12px;
}
.fields dt { font-weight: 700; }
.fields dd { margin: 0; }
.badge {
  display: inline-block;
  border: 1px solid var(--rule);
  padding: 2px 8px;
  font-size: 12px;
  text-transform: uppercase;
}
.badge.high { color: var(--verified); }
.badge.medium { color: var(--info); }
.badge.low { color: var(--urgent); }
ol, ul { padding-left: 22px; }
a { color: var(--verified); }
@media (max-width: 640px) {
  .page { padding: 24px 14px 36px; }
  h1 { font-size: 28px; }
  .fields div { grid-template-columns: 1fr; gap: 0; }
}
"""


NO_ITEMS = "\ud655\uc778\ub41c \ud56d\ubaa9\uc774 \uc5c6\uc2b5\ub2c8\ub2e4."
NO_SOURCES = "\ucd9c\ucc98\uac00 \uc5c6\uc2b5\ub2c8\ub2e4."


def escape(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def items(report: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = report.get(key) or []
    return [item for item in value if isinstance(item, dict)]


def strings(report: dict[str, Any], key: str) -> list[str]:
    value = report.get(key) or []
    return [str(item) for item in value]


def render_link(url: Any) -> str:
    if not url:
        return ""
    escaped = escape(url)
    return f'<a href="{escaped}">{escaped}</a>'


def render_badge(confidence: Any) -> str:
    value = str(confidence or "low").lower()
    if value not in {"high", "medium", "low"}:
        value = "low"
    return f'<span class="badge {value}">{escape(value)}</span>'


def render_field(label: str, value: Any, *, link: bool = False, badge: bool = False) -> str:
    if value in (None, "", []):
        return ""
    if link:
        rendered = render_link(value)
    elif badge:
        rendered = render_badge(value)
    else:
        rendered = escape(value)
    return f"<div><dt>{escape(label)}</dt><dd>{rendered}</dd></div>"


def render_cards(rows: Iterable[dict[str, Any]], *, css_class: str, fields: list[tuple[str, str, str]]) -> str:
    cards: list[str] = []
    for row in rows:
        title = escape(row.get("title") or row.get("name") or "Untitled")
        field_html = [
            render_field(label, row.get(key), link=mode == "link", badge=mode == "badge")
            for label, key, mode in fields
        ]
        field_block = "".join(part for part in field_html if part)
        cards.append(
            f'<article class="card {escape(css_class)}"><h3>{title}</h3><dl class="fields">{field_block}</dl></article>'
        )
    if not cards:
        return f'<p class="muted">{NO_ITEMS}</p>'
    return '<div class="grid">' + "".join(cards) + "</div>"


def render_list(values: list[str]) -> str:
    if not values:
        return f'<p class="muted">{NO_ITEMS}</p>'
    return "<ol>" + "".join(f"<li>{escape(value)}</li>" for value in values) + "</ol>"


def render_sources(values: list[str]) -> str:
    if not values:
        return f'<p class="muted">{NO_SOURCES}</p>'
    return "<ul>" + "".join(f"<li>{render_link(value)}</li>" for value in values) + "</ul>"


def render_report_html(report: dict[str, Any]) -> str:
    title = report.get("title") or "K-Startup Insight Report"
    date_range = report.get("date_range") or {}
    if not isinstance(date_range, dict):
        date_range = {}
    period = " - ".join(
        part for part in [str(date_range.get("start") or ""), str(date_range.get("end") or "")] if part
    )
    generated_at = report.get("generated_at") or ""
    region = report.get("region") or ""

    open_fields = [
        ("\uae30\uad00", "organization", "text"),
        ("\ub9c8\uac10", "deadline", "text"),
        ("\uae30\uac04", "application_period", "text"),
        ("\uc65c \uc911\uc694\ud55c\uac00", "why_it_matters", "text"),
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    procurement_fields = [
        ("\ubc1c\uc8fc\ucc98", "buyer", "text"),
        ("\ucc44\ub110", "procurement_channel", "text"),
        ("\uc720\ud615", "procurement_type", "text"),
        ("\uc608\uc0b0", "budget", "text"),
        ("\uc785\ucc30 \ub9c8\uac10", "bid_deadline", "text"),
        ("\uacc4\uc57d\ubc29\uc2dd", "contract_method", "text"),
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    event_fields = [
        ("\uc8fc\ucd5c", "host", "text"),
        ("\uc720\ud615", "event_type", "text"),
        ("\uc77c\uc790", "event_date", "text"),
        ("\uc2e0\uccad \ub9c8\uac10", "registration_deadline", "text"),
        ("\uc7a5\uc18c", "location", "text"),
        ("\ub300\uc0c1", "audience", "text"),
        ("\uc2e0\uccad", "registration_url", "link"),
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    recurring_fields = [
        ("\uae30\uad00", "organization", "text"),
        ("\ub9c8\uc9c0\ub9c9 \ud655\uc778", "last_seen_period", "text"),
        ("\uccb4\ud06c \uc2dc\uc810", "expected_watch_window", "text"),
        ("\uadfc\uac70", "reason", "text"),
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    source_fields = [
        ("\uc720\ud615", "source_type", "text"),
        ("\ubcfc \uc774\uc720", "why_watch", "text"),
        ("URL", "url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    vc_fields = [
        ("\ub77c\ubca8", "label", "text"),
        ("\uc2dc\uadf8\ub110", "signal", "text"),
        ("\ud54f", "fit", "text"),
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]

    sections = [
        f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>
  <main class="page">
    <header class="masthead">
      <p class="meta">{escape(region)} ? {escape(period)} ? ??? {escape(generated_at)}</p>
      <h1>{escape(title)}</h1>
    </header>
    <section class="summary">{escape(report.get("summary") or "")}</section>
""",
        "<h2>\uc9c0\uae08 \uc2e0\uccad \uac00\ub2a5\ud55c \uacf5\uace0</h2>",
        render_cards(items(report, "open_now"), css_class="open", fields=open_fields),
        "<h2>\uc62c\ud574 \uc0c8\ub85c \ud655\uc778\ub41c \uacf5\uace0</h2>",
        render_cards(items(report, "new_this_year"), css_class="open", fields=open_fields),
        "<h2>\uc785\ucc30/\uc218\uc8fc \uae30\ud68c</h2>",
        render_cards(items(report, "procurement_opportunities"), css_class="procurement", fields=procurement_fields),
        "<h2>\ud589\uc0ac\u00b7\ubaa8\uc784</h2>",
        render_cards(items(report, "event_opportunities"), css_class="event", fields=event_fields),
        "<h2>\uc62c\ud574 \ub2e4\uc2dc \ub728\uac83 \uac00\ub2a5\uc131\uc774 \ub192\uc740 \uacf5\uace0</h2>",
        render_cards(items(report, "likely_recurring"), css_class="recurring", fields=recurring_fields),
        "<h2>\uc0c8\ub85c \ubc1c\uacac\ud55c \ucd9c\ucc98</h2>",
        render_cards(items(report, "discovered_sources"), css_class="source", fields=source_fields),
        "<h2>\ud22c\uc790/VC \uc778\uc0ac\uc774\ud2b8</h2>",
        render_cards(items(report, "vc_insights"), css_class="vc", fields=vc_fields),
        "<h2>\ub2e4\uc74c \uc561\uc158</h2>",
        render_list(strings(report, "next_actions")),
        "<h2>\ucd9c\ucc98</h2>",
        render_sources(strings(report, "sources")),
        "  </main>\n</body>\n</html>\n",
    ]
    return "".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a K-startup insight report as HTML.")
    parser.add_argument("--input", required=True, help="Path to insight-report JSON.")
    parser.add_argument("--output", required=True, help="Path to output HTML.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    report = json.loads(input_path.read_text(encoding="utf-8"))
    html_text = render_report_html(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    print(f"Rendered report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
