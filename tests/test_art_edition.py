"""Art Edition v1.2.0: settings, banners and promotions API regression."""
import unittest
from fastapi.testclient import TestClient
import test_settings  # create a throwaway DB before importing server.app
from server.app import app, database, pw_hash

class ArtEditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with database() as db:
            db.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES (?,?,?)", (
                'art_admin', pw_hash('ArtAdminPassword123!'), 'admin'))
        cls.admin = TestClient(app)
        resp = cls.admin.post('/api/login', json={'username': 'art_admin', 'password': 'ArtAdminPassword123!'})
        assert resp.status_code == 200, resp.text
        cls.csrf = {'X-CSRF-Token': resp.json()['csrf']}
        cls.anon = TestClient(app)

    def test_public_content_and_brand(self):
        self.assertEqual(self.anon.get('/api/banner').status_code, 200)
        config = self.anon.get('/api/site-config').json()
        self.assertEqual(config['store_name'], "LTD's Book Store")
        self.assertTrue(config['show_coming_soon'])
        html = self.anon.get('/').text
        self.assertIn('id="themeModeBtn"', html)
        self.assertIn('id="coming-soon"', html)
        self.assertIn("LTD's Book Store", html)

    def test_admin_endpoints_require_session_and_csrf(self):
        banner = self.anon.get('/api/banner').json()
        self.assertEqual(self.anon.put('/api/admin/banner', json=banner).status_code, 401)
        self.assertEqual(self.admin.put('/api/admin/banner', json=banner).status_code, 403)
        self.assertEqual(self.anon.put('/api/admin/site-config', json={'enable_promos': True}).status_code, 401)

    def test_banner_edit_persists_and_restores(self):
        original = self.admin.get('/api/banner').json()
        updated = dict(original)
        updated['hero_title_line1'] = 'LTD Art Edition kiểm thử'
        try:
            r = self.admin.put('/api/admin/banner', json=updated, headers=self.csrf)
            self.assertEqual(r.status_code, 200, r.text)
            self.assertEqual(self.anon.get('/api/banner').json()['hero_title_line1'], updated['hero_title_line1'])
        finally:
            r = self.admin.put('/api/admin/banner', json=original, headers=self.csrf)
            self.assertEqual(r.status_code, 200, r.text)

    def test_promotion_validation_uses_server_rules(self):
        original = self.admin.get('/api/admin/site-config').json()
        conf = dict(original)
        conf['enable_promos'] = True
        conf['promos'] = [{'code': 'LTDTEST10', 'type': 'percent', 'value': 10,
                          'min_order': 100000, 'max_discount': 30000,
                          'active': True, 'show_public': False, 'label': 'Test'}]
        try:
            r = self.admin.put('/api/admin/site-config', json=conf, headers=self.csrf)
            self.assertEqual(r.status_code, 200, r.text)
            self.assertTrue(self.anon.get('/api/site-config').json()['enable_promos'])
            self.assertEqual(self.anon.get('/api/site-config').json()['public_promos'], [])
            low = self.anon.post('/api/promo/validate', json={'code': 'LTDTEST10', 'subtotal': 99000}).json()
            self.assertFalse(low['valid'])
            ok = self.anon.post('/api/promo/validate', json={'code': 'LTDTEST10', 'subtotal': 400000}).json()
            self.assertTrue(ok['valid'])
            self.assertEqual(ok['discount'], 30000)
        finally:
            r = self.admin.put('/api/admin/site-config', json=original, headers=self.csrf)
            self.assertEqual(r.status_code, 200, r.text)

if __name__ == '__main__':
    unittest.main()
