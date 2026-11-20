"""End-to-end tests for v1.3.0 workflow, inventory stock, shipping, profile, reviews, waitlist & CRM."""
import unittest
from fastapi.testclient import TestClient
import test_settings
from server.app import app, database, pw_hash


class V130WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with database() as db:
            db.execute(
                "INSERT OR IGNORE INTO users(username,password,role,full_name,phone) VALUES(?,?,?,?,?)",
                ('v130_admin', pw_hash('AdminPassV130!'), 'admin', 'Admin V130', '0901234567'),
            )
        cls.admin = TestClient(app)
        r = cls.admin.post('/api/login', json={'username': 'v130_admin', 'password': 'AdminPassV130!'})
        assert r.status_code == 200, r.text
        cls.admin_csrf = {'X-CSRF-Token': r.json()['csrf']}

        cls.buyer = TestClient(app)
        cls.buyer.post('/api/register', json={
            'username': 'v130_buyer',
            'password': 'BuyerPassword130!',
            'full_name': 'Trần Minh Khôi',
            'phone': '0918889999',
        })
        r_b = cls.buyer.post('/api/login', json={'username': 'v130_buyer', 'password': 'BuyerPassword130!'})
        assert r_b.status_code == 200, r_b.text
        cls.buyer_csrf = {'X-CSRF-Token': r_b.json()['csrf']}

    def test_profile_autofill_and_update(self):
        me = self.buyer.get('/api/me').json()
        self.assertTrue(me['authenticated'])
        self.assertEqual(me['full_name'], 'Trần Minh Khôi')
        self.assertEqual(me['phone'], '0918889999')

        upd = self.buyer.put('/api/me/profile', json={
            'full_name': 'Trần Minh Khôi',
            'phone': '0918889999',
            'address': '88 Cầu Giấy, Hà Nội',
        }, headers=self.buyer_csrf)
        self.assertEqual(upd.status_code, 200, upd.text)
        self.assertEqual(self.buyer.get('/api/me').json()['address'], '88 Cầu Giấy, Hà Nội')

    def test_stock_deduction_and_auto_restock_on_cancel(self):
        added = self.admin.post('/api/admin/books', json={
            'name': 'Chuyên đề Bất đẳng thức Lớp 9',
            'category': 'Lớp 9',
            'price': 95000,
            'image': 'assets/books/math9-set.webp',
            'description': 'Sách chuyên sâu',
            'label': 'Bồi dưỡng HSG',
            'status': 'available',
            'stock_qty': 2,
        }, headers=self.admin_csrf)
        self.assertEqual(added.status_code, 200, added.text)
        bid = added.json()['id']

        try:
            # Ordering 3 when only 2 in stock must fail with 409
            over = self.buyer.post('/api/orders', json={
                'customer_name': 'Trần Minh Khôi',
                'phone': '0918889999',
                'address': '88 Cầu Giấy, Hà Nội',
                'items': [{'book_id': bid, 'quantity': 3}],
            }, headers=self.buyer_csrf)
            self.assertEqual(over.status_code, 409)

            # Ordering all 2 reduces stock_qty to 0 and flips status to sold_out
            ok = self.buyer.post('/api/orders', json={
                'customer_name': 'Trần Minh Khôi',
                'phone': '0918889999',
                'address': '88 Cầu Giấy, Hà Nội',
                'items': [{'book_id': bid, 'quantity': 2}],
            }, headers=self.buyer_csrf)
            self.assertEqual(ok.status_code, 200, ok.text)
            b_after = next(b for b in self.buyer.get('/api/books').json() if b['id'] == bid)
            self.assertEqual(b_after['stock_qty'], 0)
            self.assertEqual(b_after['status'], 'sold_out')

            # Cancelling restores stock_qty back to 2 and status back to available
            ord_obj = next(o for o in self.buyer.get('/api/orders').json() if o['order_number'] == ok.json()['order_number'])
            c_res = self.buyer.post(f"/api/orders/{ord_obj['id']}/cancel", headers=self.buyer_csrf)
            self.assertEqual(c_res.status_code, 200)
            b_restored = next(b for b in self.buyer.get('/api/books').json() if b['id'] == bid)
            self.assertEqual(b_restored['stock_qty'], 2)
            self.assertEqual(b_restored['status'], 'available')
        finally:
            self.admin.delete(f'/api/admin/books/{bid}', headers=self.admin_csrf)

    def test_shipping_fee_threshold_and_tracking_note(self):
        orig_cfg = self.admin.get('/api/admin/site-config').json()
        cfg = dict(orig_cfg)
        cfg['enable_shipping_fee'] = True
        cfg['freeship_threshold'] = 200000
        cfg['shipping_fee'] = 25000
        try:
            self.admin.put('/api/admin/site-config', json=cfg, headers=self.admin_csrf)
            # Order 1x math6 (80,000đ < 200,000đ) -> shipping_fee = 25,000đ -> total = 105,000đ
            r_small = self.buyer.post('/api/orders', json={
                'customer_name': 'Trần Minh Khôi',
                'phone': '0918889999',
                'address': '88 Cầu Giấy, Hà Nội',
                'items': [{'book_id': 'math6', 'quantity': 1}],
            }, headers=self.buyer_csrf)
            self.assertEqual(r_small.status_code, 200, r_small.text)
            self.assertEqual(r_small.json()['shipping_fee'], 25000)
            self.assertEqual(r_small.json()['total'], 105000)

            # Admin attaches tracking_code & admin_note
            ord_obj = next(o for o in self.admin.get('/api/admin/orders').json() if o['order_number'] == r_small.json()['order_number'])
            upd = self.admin.put(f"/api/admin/orders/{ord_obj['id']}", json={
                'status': 'shipping',
                'tracking_code': 'VNPOST-8899',
                'admin_note': 'Sách đã bọc chống sốc cẩn thận',
            }, headers=self.admin_csrf)
            self.assertEqual(upd.status_code, 200)

            my_ord = next(o for o in self.buyer.get('/api/orders').json() if o['id'] == ord_obj['id'])
            self.assertEqual(my_ord['tracking_code'], 'VNPOST-8899')
            self.assertEqual(my_ord['admin_note'], 'Sách đã bọc chống sốc cẩn thận')

            # Export CSV endpoint works
            csv_res = self.admin.get('/api/admin/orders/export.csv')
            self.assertEqual(csv_res.status_code, 200)
            self.assertIn('VNPOST-8899', csv_res.text)
        finally:
            self.admin.put('/api/admin/site-config', json=orig_cfg, headers=self.admin_csrf)

    def test_verified_reviews_waitlist_and_crm(self):
        # Submit review on math6 (which v130_buyer purchased above -> verified_purchase == 1)
        rev = self.buyer.post('/api/books/math6/reviews', json={
            'rating': 5,
            'comment': 'Sách in rất rõ nét, bài tập phân dạng cực dễ hiểu!',
        }, headers=self.buyer_csrf)
        self.assertEqual(rev.status_code, 200, rev.text)

        revs = self.buyer.get('/api/books/math6/reviews').json()
        self.assertEqual(len(revs), 1)
        self.assertEqual(revs[0]['verified_purchase'], 1)
        self.assertEqual(revs[0]['rating'], 5)

        # Waitlist registration on coming-soon book
        wl = self.buyer.post('/api/waitlist', json={
            'book_id': 'hsg7',
            'customer_name': 'Phụ huynh bé Nam',
            'phone': '0977112233',
            'note': 'Báo qua Zalo giúp mình',
        })
        self.assertEqual(wl.status_code, 200, wl.text)
        self.assertGreaterEqual(wl.json()['waitlist_count'], 1)

        # Admin CRM & Analytics check
        customers = self.admin.get('/api/admin/customers').json()
        self.assertTrue(any(c['username'] == 'v130_buyer' for c in customers))
        waitlist = self.admin.get('/api/admin/waitlist').json()
        self.assertTrue(any(w['phone'] == '0977112233' for w in waitlist))
        stats = self.admin.get('/api/admin/stats').json()
        self.assertIn('top_books', stats)
        self.assertGreaterEqual(len(stats['top_books']), 1)


if __name__ == '__main__':
    unittest.main()
