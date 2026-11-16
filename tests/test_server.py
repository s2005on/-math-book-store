import json
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
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
        self.assertFalse(response.json()["api_ready"])

    def test_storefront_is_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Math Book Store", response.text)
        self.assertIn('id="productGrid"', response.text)

    def test_admin_preview_is_served(self):
        response = self.client.get("/admin.html")
        self.assertEqual(response.status_code, 200)
        self.assertIn("GIAO DIỆN MINH HỌA", response.text)

    def test_catalog_json_is_served(self):
        response = self.client.get("/catalog.json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 7)

    def test_catalog_asset_references_exist(self):
        products = json.loads((WEB / "catalog.json").read_text(encoding="utf-8"))
        for product in products:
            with self.subTest(product=product["id"]):
                self.assertTrue((WEB / product["image"]).is_file())


if __name__ == "__main__":
    unittest.main()
