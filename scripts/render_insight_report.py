#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


STYLE = """
:root {
  color-scheme: light;
  --canvas: #ffffff;
  --paper: #ffffff;
  --paper-alt: #f7f7f7;
  --ink: #222222;
  --body: #3f3f3f;
  --muted: #6a6a6a;
  --line: #dddddd;
  --primary: #ff385c;
  --primary-active: #e00b41;
  --on-primary: #ffffff;
  --radius-card: 14px;
  --radius-pill: 9999px;
  --shadow: rgba(0, 0, 0, 0.02) 0 0 0 1px, rgba(0, 0, 0, 0.04) 0 2px 6px 0, rgba(0, 0, 0, 0.1) 0 4px 8px 0;
}
body {
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font-family: "Airbnb Cereal VF", Circular, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  line-height: 1.5;
}
.page {
  max-width: 760px;
  margin: 0 auto;
  background: var(--paper);
}
.eyebrow {
  display: inline-block;
  color: var(--muted);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.32px;
  text-transform: uppercase;
}
h1, h2, h3 {
  font-family: "Airbnb Cereal VF", Circular, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  line-height: 1.2;
}
h1 {
  margin: 8px 0 12px;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 0;
}
h2 {
  margin: 0 0 12px;
  font-size: 22px;
  font-weight: 500;
  letter-spacing: -0.44px;
}
h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0;
}
.meta, .muted {
  color: var(--muted);
  font-size: 13px;
  letter-spacing: 0;
}
.summary {
  margin: 14px 0 0;
  max-width: 58ch;
  color: var(--body);
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 1.5;
}
.salutation {
  margin: 0 0 10px;
  color: var(--ink);
  font-size: 18px;
  font-weight: 600;
}
.hero-actions,
.item-actions {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  margin-top: 16px;
  flex-wrap: wrap;
}
.section {
  padding: 32px 28px;
  border-top: 1px solid var(--line);
}
.section.light,
.section.parchment,
.section.dark,
.section.dark-2,
.section.dark-3 {
  background: var(--paper);
  color: var(--ink);
}
.hero {
  padding-top: 40px;
  padding-bottom: 34px;
  border-top: 0;
}
.hero-card {
  border: 1px solid var(--line);
  border-radius: var(--radius-card);
  background: var(--paper);
  box-shadow: var(--shadow);
  padding: 24px;
}
.section-inner {
  max-width: 680px;
  margin: 0 auto;
}
.section-kicker {
  margin: 0 0 6px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0;
  text-transform: uppercase;
}
.section-lead {
  margin: 0 0 16px;
  max-width: 60ch;
  color: var(--muted);
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0;
}
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 20px;
}
.stat {
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius-card);
  background: var(--paper-alt);
}
.stat-label {
  display: block;
  color: var(--muted);
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 0;
}
.stat-value {
  display: block;
  margin-top: 4px;
  font-size: 21px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: 0;
}
.list-grid {
  display: grid;
  gap: 0;
  margin-top: 8px;
}
.list-item {
  padding: 18px 0;
  border-top: 1px solid var(--line);
}
.item-copy {
  margin: 6px 0 0;
  max-width: 62ch;
  color: var(--muted);
  font-size: 14px;
  letter-spacing: 0;
}
.meta-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
  flex-wrap: wrap;
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0;
}
.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.meta-chip + .meta-chip::before {
  content: "·";
  margin-right: 4px;
  color: currentColor;
}
.button,
.button-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-pill);
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1;
  text-decoration: none;
  transition: background-color 120ms ease, transform 120ms ease;
}
.button {
  background: var(--primary);
  color: var(--on-primary);
}
.button:hover {
  background: var(--primary-active);
}
.button-secondary {
  border: 1px solid var(--line);
  color: var(--ink);
  background: var(--paper);
}
.button:active,
.button-secondary:active {
  transform: scale(0.95);
}
a {
  color: var(--primary);
}
.section.dark a,
.section.dark-2 a,
.section.dark-3 a {
  color: var(--primary);
}
.text-list,
.source-list {
  margin: 8px 0 0;
  max-width: 680px;
  padding: 0;
  list-style: none;
}
.text-list li,
.source-list li {
  margin: 0;
  padding: 12px 0;
  border-top: 1px solid var(--line);
  font-size: 14px;
  letter-spacing: 0;
}
.text-list li:last-child,
.source-list li:last-child {
  border-bottom: 1px solid var(--line);
}
.warning-box,
.footer-note {
  max-width: 680px;
  margin: 18px 0 0;
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0;
}
.warning-box h3,
.footer-note {
  font-weight: 400;
}
.warning-box ul {
  margin: 12px 0 0;
  padding-left: 18px;
  text-align: left;
}
.warning-box li + li {
  margin-top: 8px;
}
@media (max-width: 640px) {
  .section {
    padding: 24px 18px;
  }
  .hero {
    padding-top: 30px;
    padding-bottom: 26px;
  }
  .hero-card {
    padding: 18px;
  }
  h1 { font-size: 26px; }
  h2 { font-size: 22px; }
  h3 { font-size: 16px; }
  .summary { font-size: 16px; }
  .stats-row { grid-template-columns: 1fr; }
  .meta-row { gap: 6px; }
}
"""


INLINE_STYLES = {
    "body": "margin:0;background:#ffffff;color:#222222;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.5;",
    "page": "max-width:760px;margin:0 auto;background:#ffffff;color:#222222;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;",
    "section": "padding:32px 28px;border-top:1px solid #dddddd;background:#ffffff;color:#222222;",
    "hero": "padding-top:40px;padding-bottom:34px;border-top:0;",
    "section-inner": "max-width:680px;margin:0 auto;",
    "hero-card": "border:1px solid #dddddd;border-radius:14px;background:#ffffff;box-shadow:0 2px 8px rgba(0,0,0,0.08);padding:24px;",
    "eyebrow": "display:inline-block;color:#6a6a6a;font-size:11px;font-weight:700;letter-spacing:.32px;text-transform:uppercase;",
    "salutation": "margin:0 0 10px;color:#222222;font-size:18px;font-weight:700;",
    "meta": "color:#6a6a6a;font-size:13px;letter-spacing:0;",
    "muted": "color:#6a6a6a;font-size:13px;letter-spacing:0;",
    "summary": "margin:14px 0 0;max-width:58ch;color:#3f3f3f;font-size:16px;font-weight:400;line-height:1.5;",
    "stats-row": "display:block;margin-top:20px;",
    "stat": "display:inline-block;width:29%;min-width:150px;margin:0 8px 8px 0;padding:14px;border:1px solid #dddddd;border-radius:14px;background:#f7f7f7;vertical-align:top;",
    "stat-label": "display:block;color:#6a6a6a;font-size:11px;font-weight:400;",
    "stat-value": "display:block;margin-top:4px;font-size:21px;font-weight:700;line-height:1.1;color:#222222;",
    "hero-actions": "margin-top:16px;",
    "item-actions": "margin-top:16px;",
    "section-kicker": "margin:0 0 6px;color:#6a6a6a;font-size:12px;font-weight:700;text-transform:uppercase;",
    "section-lead": "margin:0 0 16px;max-width:60ch;color:#6a6a6a;font-size:14px;font-weight:400;",
    "list-grid": "display:block;margin-top:8px;",
    "list-item": "padding:18px 0;border-top:1px solid #dddddd;",
    "item-copy": "margin:6px 0 0;max-width:62ch;color:#6a6a6a;font-size:14px;",
    "meta-row": "margin-top:8px;color:#6a6a6a;font-size:12px;",
    "meta-chip": "display:inline-block;margin:0 10px 6px 0;color:#6a6a6a;font-size:12px;",
    "button": "display:inline-block;border-radius:9999px;padding:10px 20px;background:#ff385c;color:#ffffff;font-size:14px;font-weight:600;line-height:1;text-decoration:none;margin:0 10px 8px 0;",
    "button-secondary": "display:inline-block;border:1px solid #dddddd;border-radius:9999px;padding:10px 20px;background:#ffffff;color:#222222;font-size:14px;font-weight:600;line-height:1;text-decoration:none;margin:0 10px 8px 0;",
    "text-list": "margin:8px 0 0;max-width:680px;padding:0;list-style:none;",
    "source-list": "margin:8px 0 0;max-width:680px;padding:0;list-style:none;",
    "warning-box": "max-width:680px;margin:18px 0 0;color:#6a6a6a;font-size:12px;",
    "footer-note": "max-width:680px;margin:18px 0 0;color:#6a6a6a;font-size:12px;",
}


TAG_STYLES = {
    "h1": "margin:8px 0 12px;color:#222222;font-size:28px;font-weight:700;line-height:1.2;",
    "h2": "margin:0 0 12px;color:#222222;font-size:22px;font-weight:600;line-height:1.2;",
    "h3": "margin:0;color:#222222;font-size:16px;font-weight:700;line-height:1.2;",
    "li": "margin:0;padding:12px 0;border-top:1px solid #dddddd;font-size:14px;color:#3f3f3f;",
}


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


def link_label(url: Any, fallback: str = "보기") -> str:
    if not url:
        return fallback
    parsed = urlparse(str(url))
    host = parsed.netloc.replace("www.", "")
    if not host:
        return fallback
    if "news.seoul.go.kr" in host:
        return "서울시 공고"
    if "bizinfo.go.kr" in host:
        return "Bizinfo 공고"
    if "campustown.seoul.go.kr" in host:
        return "캠퍼스타운"
    return host


def render_link(url: Any, label: str | None = None) -> str:
    if not url:
        return ""
    escaped = escape(url)
    text = escape(label or link_label(url))
    return f'<a href="{escaped}" style="color:#ff385c;text-decoration:none;">{text}</a>'


def inline_email_styles(html_text: str) -> str:
    """Add inline styles so email clients that strip <style> still render cleanly."""

    def class_replacer(match: re.Match[str]) -> str:
        tag = match.group("tag")
        before = match.group("before")
        classes = match.group("classes")
        after = match.group("after")
        styles = [INLINE_STYLES[name] for name in classes.split() if name in INLINE_STYLES]
        if tag in TAG_STYLES:
            styles.insert(0, TAG_STYLES[tag])
        if not styles:
            return match.group(0)
        return f'<{tag}{before}class="{classes}" style="{"".join(styles)}"{after}>'

    html_text = re.sub(
        r'<(?P<tag>[a-z0-9]+)(?P<before>[^>]*)class="(?P<classes>[^"]+)"(?P<after>[^>]*)>',
        class_replacer,
        html_text,
    )
    for tag, style in TAG_STYLES.items():
        html_text = re.sub(rf"<{tag}>", f'<{tag} style="{style}">', html_text)
    html_text = html_text.replace("<body>", f'<body style="{INLINE_STYLES["body"]}">')
    return html_text


def render_badge(confidence: Any) -> str:
    value = str(confidence or "low").lower()
    if value not in {"high", "medium", "low"}:
        value = "low"
    return {"high": "공식확인", "medium": "교차확인", "low": "추가확인"}.get(value, "추가확인")


def compact_text(value: Any, limit: int = 90) -> str:
    if value in (None, ""):
        return ""
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def render_field(label: str, value: Any, *, link: bool = False, badge: bool = False) -> str:
    if value in (None, "", []):
        return ""
    if link:
        rendered = render_link(value, "보기")
    elif badge:
        rendered = render_badge(value)
    else:
        rendered = escape(compact_text(value, 56))
    return f'<span class="meta-chip"><strong>{escape(label)}</strong> {rendered}</span>'


def render_cards(
    rows: Iterable[dict[str, Any]],
    *,
    css_class: str,
    fields: list[tuple[str, str, str]],
    summary_keys: list[str] | None = None,
) -> str:
    cards: list[str] = []
    for row in rows:
        title = escape(row.get("title") or row.get("name") or "Untitled")
        summary_text = ""
        for key in summary_keys or []:
            value = compact_text(row.get(key), 86)
            if value:
                summary_text = escape(value)
                break
        field_html = [
            render_field(label, row.get(key), link=mode == "link", badge=mode == "badge")
            for label, key, mode in fields
        ]
        field_block = "".join(part for part in field_html if part)
        source_url = row.get("source_url") or row.get("registration_url") or row.get("url")
        apply_url = row.get("apply_url") or row.get("registration_url")
        cards.append(
            "<article class=\"list-item\">"
            f"<h3>{title}</h3>"
            + (f'<p class="item-copy">{summary_text}</p>' if summary_text else "")
            + (f'<div class="meta-row">{field_block}</div>' if field_block else "")
            + (
                '<div class="item-actions">'
                + (f'<a class="button" href="{escape(source_url)}">공식 페이지 보기</a>' if source_url else "")
                + (f'<a class="button-secondary" href="{escape(apply_url)}">신청 링크</a>' if apply_url and apply_url != source_url else "")
                + "</div>"
                if source_url or apply_url
                else ""
            )
            + "</article>"
        )
    if not cards:
        return f'<p class="muted">{NO_ITEMS}</p>'
    return '<div class="list-grid">' + "".join(cards) + "</div>"


def limit_rows(rows: list[dict[str, Any]], count: int = 3) -> list[dict[str, Any]]:
    return rows[:count]


def render_list(values: list[str]) -> str:
    if not values:
        return f'<p class="muted">{NO_ITEMS}</p>'
    return '<ul class="text-list">' + "".join(f"<li>{escape(compact_text(value, 120))}</li>" for value in values) + "</ul>"


def render_sources(values: list[str]) -> str:
    if not values:
        return f'<p class="muted">{NO_SOURCES}</p>'
    return '<ul class="source-list">' + "".join(f"<li>{render_link(value, link_label(value))}</li>" for value in values) + "</ul>"


def render_section(title: str, content: str, *, theme: str, kicker: str = "", lead: str = "") -> str:
    return (
        f'<section class="section {escape(theme)}"><div class="section-inner">'
        + (f'<p class="section-kicker">{escape(kicker)}</p>' if kicker else "")
        + f"<h2>{escape(title)}</h2>"
        + (f'<p class="section-lead">{escape(lead)}</p>' if lead else "")
        + content
        + "</div></section>"
    )


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
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    procurement_fields = [
        ("\ubc1c\uc8fc\ucc98", "buyer", "text"),
        ("\uc785\ucc30 \ub9c8\uac10", "bid_deadline", "text"),
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    event_fields = [
        ("\uc8fc\ucd5c", "host", "text"),
        ("\uc77c\uc790", "event_date", "text"),
        ("\uc2e0\uccad \ub9c8\uac10", "registration_deadline", "text"),
        ("\uc2e0\uccad", "registration_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    recurring_fields = [
        ("\uae30\uad00", "organization", "text"),
        ("\uccb4\ud06c \uc2dc\uc810", "expected_watch_window", "text"),
        ("\ucd9c\ucc98", "source_url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    source_fields = [
        ("\uc720\ud615", "source_type", "text"),
        ("URL", "url", "link"),
        ("\uc2e0\ub8b0\ub3c4", "confidence", "badge"),
    ]
    vc_fields = [
        ("\ub77c\ubca8", "label", "text"),
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
    <section class="section light hero">
      <div class="section-inner">
      <div class="hero-card">
      <span class="eyebrow">Startup Support Brief</span>
        <p class="salutation">친애하는 박상희 대표님께 🥰</p>
        <h1>{escape(title)}</h1>
        <p class="meta">{escape(region)} · 조사 기간 {escape(period)} · 검증일 {escape(generated_at)}</p>
      <section class="summary">{escape(compact_text(report.get("summary") or "", 150))}</section>
      <div class="stats-row">
        <article class="stat">
          <span class="stat-label">Open Now</span>
          <span class="stat-value">{len(open_now_items)}건</span>
        </article>
        <article class="stat">
          <span class="stat-label">Watchlist</span>
          <span class="stat-value">{len(recurring_items) + len(source_items)}건</span>
        </article>
        <article class="stat">
          <span class="stat-label">Signals</span>
          <span class="stat-value">{len(vc_items)}건</span>
        </article>
      </div>
      <div class="hero-actions">
        <a class="button" href="#open-now">주요 공고</a>
        <a class="button-secondary" href="#sources">공식 출처</a>
      </div>
      </div>
      </div>
    </section>
""",
        '<div id="open-now"></div>'
        + render_section(
            "지금 신청 가능한 공고",
            render_cards(limit_rows(items(report, "open_now")), css_class="open", fields=open_fields, summary_keys=["why_it_matters", "benefit_summary"]),
            theme="parchment",
            kicker="Open Now",
            lead="메일에서는 우선순위 3건만 보여줍니다.",
        ),
        render_section(
            "올해 새로 확인된 공고",
            render_cards(limit_rows(items(report, "new_this_year"), 2), css_class="open", fields=open_fields, summary_keys=["why_it_matters", "benefit_summary"]),
            theme="dark",
            kicker="New This Year",
            lead="이번 조사에서 새로 확인한 공고입니다.",
        ),
        render_section(
            "올해 다시 뜰 가능성이 높은 공고",
            render_cards(limit_rows(items(report, "likely_recurring"), 2), css_class="recurring", fields=recurring_fields, summary_keys=["reason", "last_seen_period"]),
            theme="light",
            kicker="Watchlist",
            lead="다시 확인할 가치가 큰 반복 후보입니다.",
        ),
        render_section(
            "새로 발견한 출처",
            render_cards(limit_rows(items(report, "discovered_sources"), 3), css_class="source", fields=source_fields, summary_keys=["why_watch"]),
            theme="dark-2",
            kicker="Sources",
            lead="모니터링할 공식 출처입니다.",
        ),
        render_section(
            "투자/VC 인사이트",
            render_cards(limit_rows(items(report, "vc_insights"), 2), css_class="vc", fields=vc_fields, summary_keys=["signal"]),
            theme="light",
            kicker="Signals",
            lead="파트너십 판단에 보탤 짧은 시그널입니다.",
        ),
        render_section(
            "다음 액션",
            render_list(strings(report, "next_actions")),
            theme="parchment",
            kicker="Next",
            lead="바로 실행 순서로 보면 좋습니다.",
        ),
        '<div id="sources"></div>'
        + render_section(
            "출처",
            render_sources(strings(report, "sources"))
            + (
                '<section class="warning-box"><h3>주의</h3><ul>'
                + "".join(f"<li>{escape(item)}</li>" for item in warnings)
                + "</ul></section>"
                if warnings
                else ""
            )
            + '<p class="footer-note">이 리포트는 공식 페이지와 공공 포털 기준으로 정리했으며, 실제 지원 전에는 각 공고의 마감 시각과 세부 자격요건을 다시 확인하는 것을 권장합니다.</p>',
            theme="dark-3",
            kicker="Verification",
            lead="모든 판단은 공식 페이지를 최종 기준으로 다시 확인하는 것을 전제로 합니다.",
        ),
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
    html_text = inline_email_styles(render_report_html(report))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    print(f"Rendered report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
