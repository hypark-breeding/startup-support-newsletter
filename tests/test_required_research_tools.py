from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RequiredResearchToolsTests(unittest.TestCase):
    def test_manifest_requires_gpt_researcher_and_crawl4ai(self) -> None:
        manifest = json.loads((ROOT / "skill-manifest.json").read_text(encoding="utf-8"))

        packages = manifest["install"]["required_python_packages"]
        package_names = {package["name"] for package in packages}

        self.assertIn("gpt-researcher", package_names)
        self.assertIn("crawl4ai", package_names)
        for package in packages:
            if package["name"] in {"gpt-researcher", "crawl4ai"}:
                self.assertTrue(package["required"])

    def test_install_script_installs_required_research_tools(self) -> None:
        script = (ROOT / "scripts" / "install_skill.sh").read_text(encoding="utf-8")

        self.assertIn("REQUIRED_PYTHON_PACKAGES", script)
        self.assertIn("gpt-researcher", script)
        self.assertIn("crawl4ai", script)
        self.assertIn("install_required_python_tools", script)
        self.assertIn("crawl4ai-setup", script)


if __name__ == "__main__":
    unittest.main()
