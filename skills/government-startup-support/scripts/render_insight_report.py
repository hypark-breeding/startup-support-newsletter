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
  --canvas: #f6efe4;
  --paper: #fffaf2;
  --paper-strong: #fffdf8;
  --ink: #17352d;
  --muted: #6f6a5f;
  --rule: #dbc7aa;
  --accent: #8c6a43;
  --accent-soft: #efe1cf;
  --deadline: #d96c45;
  --verified: #2d7a63;
  --info: #4c667f;
  --shadow: 0 10px 28px rgba(23, 53, 45, 0.06);
}
body {
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font-family: "Pretendard", "Pretendard Variable", "Noto Sans KR", Arial, sans-serif;
  line-height: 1.52;
}
.page {
  max-width: 940px;
  margin: 0 auto;
  padding: 30px 18px 48px;
}
.masthead {
  background:
    radial-gradient(circle at top right, rgba(217, 108, 69, 0.12), transparent 34%),
    radial-gradient(circle at left 22%, rgba(140, 106, 67, 0.10), transparent 28%),
    linear-gradient(180deg, #fffdf8 0%, #fff8ef 100%);
  border: 1px solid var(--rule);
  border-radius: 24px;
  box-shadow: var(--shadow);
  padding: 24px 24px 20px;
  margin-bottom: 20px;
  overflow: hidden;
}
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(140, 106, 67, 0.10);
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.eyebrow::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--deadline);
}
h1, h2, h3 {
  font-family: Fraunces, Georgia, serif;
  letter-spacing: 0;
  line-height: 1.2;
}
h1 {
  font-size: 36px;
  margin: 14px 0 10px;
  max-width: 700px;
}
h2 {
  font-size: 22px;
  border-bottom: 1px solid var(--rule);
  padding-bottom: 8px;
  margin: 28px 0 8px;
}
h3 {
  font-size: 18px;
  margin: 0 0 8px;
}
.meta, .muted {
  color: var(--muted);
  font-size: 13px;
}
.masthead-copy {
  max-width: 720px;
}
.masthead .meta {
  margin-top: 0;
}
.summary {
  background: var(--paper-strong);
  border: 1px solid var(--rule);
  border-radius: 16px;
  padding: 14px 16px;
  margin: 14px 0 16px;
  box-shadow: 0 6px 18px rgba(23, 53, 45, 0.04);
}
.brief-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-top: 12px;
}
.brief-note {
  background: rgba(255, 250, 242, 0.92);
  border: 1px solid var(--rule);
  border-radius: 16px;
  padding: 11px 12px;
}
.brief-label {
  display: block;
  color: var(--accent);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.brief-copy {
  display: block;
  margin-top: 6px;
  color: var(--ink);
  font-size: 12px;
  line-height: 1.45;
}
.grid {
  display: grid;
  gap: 10px;
}
.section-intro {
  margin: 0 0 10px;
  color: var(--muted);
  font-size: 12px;
}
.card {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 16px;
  padding: 12px 14px 11px;
  box-shadow: 0 6px 16px rgba(23, 53, 45, 0.035);
  position: relative;
  overflow: hidden;
}
.card::before {
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: var(--info);
}
.card.open::before { background: var(--verified); }
.card.procurement::before { background: var(--deadline); }
.card.recurring::before { background: var(--accent); }
.card.event::before { background: var(--info); }
.card.vc::before { background: var(--accent); }
.card.source::before { background: var(--accent); }
.card h3 {
  max-width: 640px;
}
.fields {
  display: grid;
  gap: 4px;
  margin: 0;
}
.fields div {
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 8px;
}
.fields dt {
  font-weight: 700;
  color: var(--accent);
  font-size: 11px;
  line-height: 1.35;
}
.fields dd {
  margin: 0;
  font-size: 11px;
  line-height: 1.45;
}
.badge {
  display: inline-block;
  border: 1px solid currentColor;
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.65);
}
.badge.high { color: var(--verified); }
.badge.medium { color: var(--info); }
.badge.low { color: var(--deadline); }
.action-list,
.source-list {
  background: var(--paper-strong);
  border: 1px solid var(--rule);
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(23, 53, 45, 0.035);
  padding: 12px 14px 12px 18px;
}
ol, ul { padding-left: 22px; }
li + li { margin-top: 6px; }
a {
  color: var(--verified);
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
  word-break: break-word;
}
.warning-box {
  margin-top: 18px;
  background: #fff6ee;
  border: 1px solid #ecc8b3;
  border-radius: 16px;
  padding: 12px 14px;
}
.warning-box h3 {
  margin-bottom: 8px;
  font-size: 15px;
}
.footer-note {
  margin-top: 14px;
  color: var(--muted);
  font-size: 11px;
}
@media (max-width: 640px) {
  .page { padding: 20px 12px 32px; }
  .masthead { padding: 18px 16px 16px; border-radius: 18px; }
  h1 { font-size: 28px; }
  .brief-grid { grid-template-columns: 1fr; }
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
    return '<ol class="action-list">' + "".join(f"<li>{escape(value)}</li>" for value in values) + "</ol>"


def render_sources(values: list[str]) -> str:
    if not values:
        return f'<p class="muted">{NO_SOURCES}</p>'
    return '<ul class="source-list">' + "".join(f"<li>{render_link(value)}</li>" for value in values) + "</ul>"


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
    open_now_items = items(report, "open_now")
    recurring_items = items(report, "likely_recurring")
    source_items = items(report, "discovered_sources")
    vc_items = items(report, "vc_insights")
    warnings = strings(report, "warnings")

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
      <span class="eyebrow">Seoul PetTech Brief</span>
      <div class="masthead-copy">
        <h1>{escape(title)}</h1>
        <p class="meta">{escape(region)} · 조사 기간 {escape(period)} · 검증일 {escape(generated_at)}</p>
      </div>
      <section class="summary">{escape(report.get("summary") or "")}</section>
      <div class="brief-grid">
        <article class="brief-note">
          <span class="brief-label">Open Now</span>
          <span class="brief-copy">즉시 검토 가능한 공고는 {len(open_now_items)}건입니다. 서울 전용과 서울 기업이 바로 지원 가능한 중앙부처 공고를 함께 담았습니다.</span>
        </article>
        <article class="brief-note">
          <span class="brief-label">Where To Watch</span>
          <span class="brief-copy">반복 후보는 {len(recurring_items)}건, 핵심 출처는 {len(source_items)}곳입니다. 펫테크 단독 공고보다 거점·트랙 중심 모니터링이 중요합니다.</span>
        </article>
        <article class="brief-note">
          <span class="brief-label">Partner Signal</span>
          <span class="brief-copy">투자·파트너십 인사이트는 {len(vc_items)}건입니다. 서울에선 AI, 바이오, 소셜벤처 설명력이 붙을수록 연결 가능성이 높습니다.</span>
        </article>
      </div>
    </header>
""",
        "<h2>지금 신청 가능한 공고</h2>",
        '<p class="section-intro">마감이 가깝거나 현재 접수 중인 항목만 우선 배치했습니다. 서울 전용 공고와 서울 기업이 바로 지원 가능한 중앙부처 공고를 함께 담았습니다.</p>',
        render_cards(items(report, "open_now"), css_class="open", fields=open_fields),
        "<h2>올해 새로 확인된 공고</h2>",
        '<p class="section-intro">이미 마감됐더라도 서울 권역 펫테크가 연결하기 좋은 기관과 프로그램 축을 보여주는 항목입니다.</p>',
        render_cards(items(report, "new_this_year"), css_class="open", fields=open_fields),
        "<h2>입찰/수주 기회</h2>",
        render_cards(items(report, "procurement_opportunities"), css_class="procurement", fields=procurement_fields),
        "<h2>행사·모임</h2>",
        render_cards(items(report, "event_opportunities"), css_class="event", fields=event_fields),
        "<h2>올해 다시 뜰 가능성이 높은 공고</h2>",
        '<p class="section-intro">지금 열려 있다고 보기 어렵지만, 시기와 운영 패턴상 다시 확인할 가치가 큰 트랙입니다.</p>',
        render_cards(items(report, "likely_recurring"), css_class="recurring", fields=recurring_fields),
        "<h2>새로 발견한 출처</h2>",
        render_cards(items(report, "discovered_sources"), css_class="source", fields=source_fields),
        "<h2>투자/VC 인사이트</h2>",
        render_cards(items(report, "vc_insights"), css_class="vc", fields=vc_fields),
        "<h2>다음 액션</h2>",
        render_list(strings(report, "next_actions")),
        "<h2>출처</h2>",
        render_sources(strings(report, "sources")),
        (
            '<section class="warning-box"><h3>주의</h3><ul>'
            + "".join(f"<li>{escape(item)}</li>" for item in warnings)
            + "</ul></section>"
            if warnings
            else ""
        ),
        '<p class="footer-note">이 리포트는 공식 페이지와 공공 포털 기준으로 정리했으며, 실제 지원 전에는 각 공고의 마감 시각과 세부 자격요건을 다시 확인하는 것을 권장합니다.</p>',
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
