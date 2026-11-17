"""Regression checks for LTD Book Store academic documentation structure."""
from pathlib import Path
from urllib.parse import unquote
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "VERSION", "CHANGELOG.md",
    "docs/01-project-charter.md", "docs/02-requirements.md",
    "docs/03-system-design.md", "docs/04-wbs.md",
    "docs/05-schedule.md", "docs/06-scrum-team.md",
    "docs/07-sprint-0-backlog.md", "docs/08-mvp-demo.md",
    "docs/B2-REPORT.md", "docs/MIDTERM.md",
    "docs/ACADEMIC-TRACEABILITY.md", "docs/VERSION-INTAKE.md",
    "docs/SPRINT-TRACKER.md", "docs/TEST-PLAN.md",
    "docs/QUALITY.md", "docs/RISKS.md",
    "docs/FINAL-REPORT.md", "docs/FINAL-HANDOVER.md",
    "docs/evidence/README.md", ".github/workflows/ci.yml",
    ".github/workflows/release.yml", "scripts/package.py",
    "scripts/verify_package.py"
]

LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
NEW_DOCUMENTS = [
    "README.md", "docs/ACADEMIC-TRACEABILITY.md",
    "docs/VERSION-INTAKE.md", "docs/SPRINT-TRACKER.md",
    "docs/MIDTERM.md", "docs/B2-REPORT.md",
    "docs/FINAL-REPORT.md", "docs/FINAL-HANDOVER.md",
    "docs/03-system-design.md", "docs/TEST-PLAN.md",
    "docs/QUALITY.md", "docs/RISKS.md"
]

class AcademicDocsTests(unittest.TestCase):
    def test_expected_repo_structure_exists(self):
        missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
        self.assertEqual(missing, [], f"Missing academic artifacts: {missing}")

    def test_readme_has_correct_brand_and_repository(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("LTD's Book Store", readme)
        self.assertIn("s2005on/LTDs-Book-Store", readme)

    def test_local_markdown_links_resolve(self):
        broken = []
        for relative in NEW_DOCUMENTS:
            path = ROOT / relative
            text = path.read_text(encoding="utf-8")
            for raw in LINK_PATTERN.findall(text):
                dest = raw.split("#", 1)[0].strip()
                if not dest or "://" in dest or dest.startswith(("mailto:", "/")):
                    continue
                target = (path.parent / unquote(dest)).resolve()
                if not target.is_relative_to(ROOT.resolve()) or not target.exists():
                    broken.append((relative, raw))
        self.assertEqual(broken, [], f"Broken local Markdown links: {broken}")

    def test_no_unrelated_project_branding_in_current_sources(self):
        forbidden = ("VNU" + " Food Hola", "vnu" + "-food-hola")
        roots = [ROOT / p for p in ("docs", ".github", "server", "scripts", "tests")]
        files = [ROOT / p for p in ("README.md", "START-HERE.md", "CHANGELOG.md", "VERIFICATION.md")]
        files += [
            path for directory in roots for path in directory.rglob("*")
            if path.is_file() and path.suffix.lower() in {".md", ".py", ".js", ".css", ".html", ".yml", ".yaml", ".json", ".svg", ".cjs"}
            and "data" not in path.parts and "__pycache__" not in path.parts
        ]
        violations = []
        for path in files:
            content = path.read_text(encoding="utf-8", errors="replace")
            if any(phrase.lower() in content.lower() for phrase in forbidden):
                violations.append(str(path.relative_to(ROOT)))
        self.assertEqual(violations, [], f"Cross-project references remain: {violations}")

    def test_release_intake_avoids_automatic_publishing(self):
        intake = (ROOT / "docs/VERSION-INTAKE.md").read_text(encoding="utf-8")
        for token in ("SHA-256", "Pull Request", "VERSION", ".env", "server/data/"):
            self.assertIn(token, intake)

if __name__ == "__main__":
    unittest.main()
