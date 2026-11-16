"""Branding regression checks for the current GitHub source (v0.5.1)."""
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from server.app import app

ROOT=Path(__file__).resolve().parents[1]

class LtdBrandingTests(unittest.TestCase):
    def test_display_name_all_interfaces(self):
        for page in ["index.html","login.html","account.html","admin.html"]:
            with self.subTest(page=page):
                txt=(ROOT/"server"/"web"/page).read_text(encoding="utf-8")
                self.assertIn("LTD's Book Store",txt)
                self.assertNotIn("Math Book Store",txt)

    def test_package_filename_uses_ltd(self):
        assert "LTDs-Book-Store" in (ROOT/"scripts/package.py").read_text(encoding="utf-8")
        assert "LTDs-Book-Store" in (ROOT/"scripts/verify_package.py").read_text(encoding="utf-8")

    def test_health_slug(self):
        data=TestClient(app).get("/health").json()
        self.assertEqual(data["project"],"ltds-book-store")

if __name__=="__main__":
    unittest.main()
