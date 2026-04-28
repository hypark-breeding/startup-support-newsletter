from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


render = load_module("render_insight_report", ROOT / "scripts" / "render_insight_report.py")


def sample_report() -> dict:
    return {
        "title": "\uc11c\uc6b8 AI \uc2a4\ud0c0\ud2b8\uc5c5 \uae30\ud68c \ub9ac\ud3ec\ud2b8",
        "region": "seoul",
        "date_range": {"start": "2025-04-28", "end": "2026-04-28"},
        "generated_at": "2026-04-28",
        "summary": "\uc62c\ud574 \uc5f4\ub9b0 \uacf5\uace0\uc640 \uc791\ub144 \ubc18\ubcf5 \ud6c4\ubcf4\ub97c \ud568\uaed8 \ubcf8\ub2e4.",
        "open_now": [
            {
                "title": "AI PoC \uc9c0\uc6d0\uc0ac\uc5c5",
                "organization": "\uc11c\uc6b8\uc2dc",
                "deadline": "2026-05-10",
                "why_it_matters": "\ucd08\uae30 PoC \ube44\uc6a9\uc744 \uc904\uc778\ub2e4.",
                "source_url": "https://example.org/notice",
                "confidence": "high",
            }
        ],
        "likely_recurring": [
            {
                "title": "\uc791\ub144 \ucea0\ud37c\uc2a4\ud0c0\uc6b4 \uc785\uc8fc\uae30\uc5c5 \ubaa8\uc9d1",
                "organization": "\ucea0\ud37c\uc2a4\ud0c0\uc6b4",
                "last_seen_period": "2025-05",
                "expected_watch_window": "2026-05",
                "reason": "\ucd5c\uadfc 3\ub144\uac04 5\uc6d4 \ubaa8\uc9d1",
                "source_url": "https://example.org/2025",
                "confidence": "medium",
            }
        ],
        "vc_insights": [
            {
                "name": "AI \uc804\ubb38 AC",
                "signal": "\ucd08\uae30 AI B2B \ud300\uc5d0 \uad00\uc2ec",
                "fit": "PoC \uc2e4\uc801 \ubcf4\uc720 \ud300",
                "source_url": "https://example.org/vc",
                "confidence": "medium",
            }
        ],
        "next_actions": ["5\uc6d4 \uccab\uc9f8 \uc8fc \uacf5\uace0 \uc7ac\ud655\uc778", "PoC \uc608\uc0b0\ud45c \uc900\ube44"],
        "sources": ["https://example.org/notice", "https://example.org/vc"],
    }


class RenderInsightReportTests(unittest.TestCase):
    def test_render_report_includes_designed_sections_and_escapes_html(self) -> None:
        report = sample_report()
        report["summary"] = "<script>alert('x')</script>"

        html = render.render_report_html(report)

        self.assertIn("\uc9c0\uae08 \uc2e0\uccad \uac00\ub2a5\ud55c \uacf5\uace0", html)
        self.assertIn("\uc62c\ud574 \ub2e4\uc2dc \ub728\uac83 \uac00\ub2a5\uc131\uc774 \ub192\uc740 \uacf5\uace0", html)
        self.assertIn("\ud22c\uc790/VC \uc778\uc0ac\uc774\ud2b8", html)
        self.assertIn("\ub2e4\uc74c \uc561\uc158", html)
        self.assertIn("&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;", html)
        self.assertNotIn("<script>alert('x')</script>", html)


if __name__ == "__main__":
    unittest.main()
