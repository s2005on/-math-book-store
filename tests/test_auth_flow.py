"""Check independent login/register pages and customer profile migration/validation."""
import unittest
from fastapi.testclient import TestClient
import test_settings
from server.app import app, database, pw_hash


class AuthRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_pages_are_separate_and_are_served(self):
        sign_in = self.client.get('/login.html')
        sign_up = self.client.get('/register.html')
        css = self.client.get('/auth.css')
        js = self.client.get('/auth.js')
        self.assertEqual([sign_in.status_code, sign_up.status_code, css.status_code, js.status_code], [200]*4)
        self.assertIn('data-mode="login"', sign_in.text)
        self.assertIn('data-mode="register"', sign_up.text)
        self.assertNotIn('id="phone"', sign_in.text)
        self.assertIn('id="phone"', sign_up.text)
        self.assertIn('name="phone"', sign_up.text)
        self.assertIn('required', sign_up.text)
        self.assertIn('confirm_password', sign_up.text)
        self.assertNotIn('accounts.google.com', sign_in.text + sign_up.text)
        self.assertNotIn('facebook.com', sign_in.text + sign_up.text)

    def test_phone_and_full_name_are_required_and_checked_server_side(self):
        base = {'username':'phone_required_user', 'password':'StrongPassword123!'}
        self.assertEqual(self.client.post('/api/register', json=base).status_code, 422)
        self.assertEqual(self.client.post('/api/register', json={**base,'phone':'0987654321'}).status_code, 422)
        for phone in ('', '1234567890', '098123', '0281234567', '098765432a'):
            with self.subTest(phone=phone):
                r = self.client.post('/api/register', json={**base, 'full_name':'Khách Hàng', 'phone':phone})
                self.assertIn(r.status_code, (400, 422))

    def test_signup_saves_profile_and_can_login(self):
        payload={'username':'auth_customer_test','password':'CustomerTest!123',
                 'full_name':'  Nguyễn   Văn   Bình  ', 'phone':'0912345678'}
        r=self.client.post('/api/register',json=payload)
        self.assertEqual(r.status_code,200,r.text)
        with database() as db:
            row=db.execute('SELECT full_name,phone,role FROM users WHERE username=?',('auth_customer_test',)).fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row['full_name'],'Nguyễn Văn Bình')
            self.assertEqual(row['phone'],'0912345678')
            self.assertEqual(row['role'],'customer')
        login=self.client.post('/api/login',json={'username':'auth_customer_test','password':'CustomerTest!123'})
        self.assertEqual(login.status_code,200,login.text)
        self.assertTrue(self.client.get('/api/me').json()['authenticated'])
        self.assertEqual(self.client.post('/api/register',json=payload).status_code,409)

    def test_existing_accounts_without_phone_still_work(self):
        with database() as db:
            db.execute('INSERT OR IGNORE INTO users(username,password,role) VALUES (?,?,?)',
                       ('legacy_customer_test',pw_hash('LegacyPassword123!'),'customer'))
        r=TestClient(app).post('/api/login',json={'username':'legacy_customer_test','password':'LegacyPassword123!'})
        self.assertEqual(r.status_code,200,r.text)

if __name__=='__main__':
    unittest.main()
