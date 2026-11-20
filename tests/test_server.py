import json
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
import test_settings  # isolate local test database
from server.app import app

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "server" / "web"


class ServerSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint_reports_ui_stage(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertTrue(response.json()["api_ready"])
        self.assertEqual(response.json()["stage"], "art-edition-v1.2.1")

    def test_storefront_is_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("LTD's Book Store", response.text)
        self.assertIn('id="productGrid"', response.text)

    def test_admin_preview_is_served(self):
        response = self.client.get("/admin.html")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bảng điều khiển Moderator", response.text)
        self.assertIn("bookStatus", response.text)

    def test_catalog_json_is_served(self):
        response = self.client.get("/catalog.json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 9)

    def test_catalog_asset_references_exist(self):
        products = json.loads((WEB / "catalog.json").read_text(encoding="utf-8"))
        for product in products:
            with self.subTest(product=product["id"]):
                self.assertTrue((WEB / product["image"]).is_file())


if __name__ == "__main__":
    unittest.main()
