from __future__ import annotations

import json
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class NationwideDiscoveryScopeTests(unittest.TestCase):
    def test_manifest_declares_nationwide_url_optional_discovery(self) -> None:
        manifest = json.loads((ROOT / "skill-manifest.json").read_text(encoding="utf-8"))
        metadata = manifest["metadata"]
        assumptions = metadata["input_assumptions"]

        self.assertIn("national", metadata["coverage"])
        self.assertTrue(assumptions["user_urls_optional"])
        self.assertTrue(assumptions["discover_sources_when_urls_missing"])
        self.assertEqual("national", assumptions["default_region"])

    def test_regions_include_nationwide_and_all_major_korean_regions(self) -> None:
        data = yaml.safe_load((ROOT / "data" / "regions.yaml").read_text(encoding="utf-8"))
        national = data["regions"]["national"]
        included = set(national["included_regions"])

        expected = {
            "\uc11c\uc6b8", "\ubd80\uc0b0", "\ub300\uad6c", "\uc778\ucc9c", "\uad11\uc8fc", "\ub300\uc804", "\uc6b8\uc0b0", "\uc138\uc885",
            "\uacbd\uae30", "\uac15\uc6d0", "\ucda9\ubd81", "\ucda9\ub0a8", "\uc804\ubd81", "\uc804\ub0a8", "\uacbd\ubd81", "\uacbd\ub0a8", "\uc81c\uc8fc",
        }
        self.assertTrue(expected.issubset(included))
        self.assertIn("\uc804\uad6d", national["aliases"])
        self.assertIn("nationwide", national["aliases"])

    def test_national_source_seeds_exist_for_no_url_searches(self) -> None:
        data = yaml.safe_load((ROOT / "data" / "sources.yaml").read_text(encoding="utf-8"))
        sources = {source["id"]: source for source in data["sources"]}

        for source_id in {
            "bizinfo-national",
            "k-startup-national",
            "ccei-national",
            "smes-go-kr-policy-notices",
            "g2b-bid-notices",
            "data-go-kr-g2b-bid-api",
        }:
            self.assertIn(source_id, sources)
            self.assertEqual("national", sources[source_id]["region"])

    def test_skill_and_docs_do_not_require_user_provided_urls(self) -> None:
        skill = (ROOT / "skills" / "government-startup-support" / "SKILL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "docs" / "collection-workflow.md").read_text(encoding="utf-8")
        research = (ROOT / "docs" / "research-insights.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.ko.md").read_text(encoding="utf-8")

        self.assertIn("Default coverage is nationwide", skill)
        self.assertIn("If the user does not provide URLs", skill)
        self.assertIn("If the user provides no URL", workflow)
        self.assertIn("No user-provided URL is required", research)
        self.assertNotIn("Initial coverage is Seoul", skill)
        self.assertNotIn("\ucd08\uae30 \ubc94\uc704\ub294 \uc11c\uc6b8", readme)


if __name__ == "__main__":
    unittest.main()
