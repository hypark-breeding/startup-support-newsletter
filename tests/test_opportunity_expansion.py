from __future__ import annotations

import json
import importlib.util
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


render = load_module("render_insight_report", ROOT / "scripts" / "render_insight_report.py")


class OpportunityExpansionTests(unittest.TestCase):
    def test_keywords_include_procurement_events_and_meetups(self) -> None:
        data = yaml.safe_load((ROOT / "data" / "keywords.yaml").read_text(encoding="utf-8"))
        groups = data["keyword_groups"]

        self.assertIn("procurement", groups)
        self.assertIn("events", groups)
        self.assertIn("meetups", groups)
        self.assertIn("\uc785\ucc30\uacf5\uace0", groups["procurement"])
        self.assertIn("\ub124\ud2b8\uc6cc\ud0b9", groups["meetups"])
        self.assertNotIn("\uc785\ucc30\uacf5\uace0", groups.get("negative_filters", []))

    def test_sources_include_procurement_and_event_feeds(self) -> None:
        data = yaml.safe_load((ROOT / "data" / "sources.yaml").read_text(encoding="utf-8"))
        sources = {source["id"]: source for source in data["sources"]}

        expected_ids = {
            "g2b-bid-notices",
            "data-go-kr-g2b-bid-api",
            "seoul-contract-market",
            "k-startup-events",
            "startup-alliance-events",
        }
        self.assertTrue(expected_ids.issubset(sources))
        self.assertIn("procurement", sources["g2b-bid-notices"]["topics"])
        self.assertIn("events", sources["startup-alliance-events"]["topics"])
        self.assertIn("meetups", sources["startup-alliance-events"]["topics"])

    def test_manifest_lists_procurement_and_event_schemas_and_docs(self) -> None:
        manifest = json.loads((ROOT / "skill-manifest.json").read_text(encoding="utf-8"))

        self.assertIn("docs/procurement-opportunities.md", manifest["doc_paths"])
        self.assertIn("docs/events-and-meetups.md", manifest["doc_paths"])
        self.assertIn("schemas/procurement-opportunity.schema.json", manifest["schema_paths"])
        self.assertIn("schemas/event-opportunity.schema.json", manifest["schema_paths"])

    def test_renderer_includes_procurement_and_event_sections(self) -> None:
        report = {
            "title": "Integrated opportunity report",
            "region": "seoul",
            "date_range": {"start": "2025-04-28", "end": "2026-04-28"},
            "generated_at": "2026-04-28",
            "summary": "Support programs, bids, and events together.",
            "procurement_opportunities": [
                {
                    "title": "AI search PoC service bid",
                    "buyer": "Seoul Metropolitan Government",
                    "bid_deadline": "2026-05-20",
                    "source_url": "https://contract.seoul.go.kr/",
                    "confidence": "high",
                }
            ],
            "event_opportunities": [
                {
                    "title": "Startup networking day",
                    "host": "Startup Alliance",
                    "event_date": "2026-05-28",
                    "source_url": "https://startupall.kr/",
                    "confidence": "medium",
                }
            ],
            "sources": ["https://contract.seoul.go.kr/", "https://startupall.kr/"],
        }

        html = render.render_report_html(report)

        self.assertIn("\uc785\ucc30/\uc218\uc8fc \uae30\ud68c", html)
        self.assertIn("\ud589\uc0ac\u00b7\ubaa8\uc784", html)
        self.assertIn("AI search PoC service bid", html)
        self.assertIn("Startup networking day", html)


if __name__ == "__main__":
    unittest.main()
