"""End-to-end local API checks: customer orders, admin operations and stock rules."""
import unittest
from fastapi.testclient import TestClient
import test_settings  # ensures a temporary db before importing the server
from server.app import app, database, pw_hash


class OrderFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with database() as db:
            db.execute('INSERT OR IGNORE INTO users(username,password,role) VALUES(?,?,?)',
                       ('order_admin', pw_hash('admin-test-pass-123'), 'admin'))
        cls.customer = TestClient(app)
        cls.admin = TestClient(app)
        r = cls.customer.post('/api/register',json={'username':'buyer_test','password':'BuyerTest-123','full_name':'Khách thử nghiệm','phone':'0987654321'})
        assert r.status_code in (200,409),r.text
        r = cls.customer.post('/api/login',json={'username':'buyer_test','password':'BuyerTest-123','full_name':'Khách thử nghiệm','phone':'0987654321'})
        assert r.status_code == 200,r.text
        cls.customer_csrf = r.json()['csrf']
        r = cls.admin.post('/api/login',json={'username':'order_admin','password':'admin-test-pass-123'})
        assert r.status_code == 200,r.text
        cls.admin_csrf = r.json()['csrf']

    def test_order_created_and_status_management(self):
        payload={'customer_name':'Khach thu nghiem','phone':'0987654321',
                 'address':'12 Duong thu nghiem, Ha Noi','note':'Giao gio hanh chinh',
                 'items':[{'book_id':'hsg8','quantity':2}]}
        self.assertEqual(self.customer.post('/api/orders',json=payload).status_code,403)
        r=self.customer.post('/api/orders',json=payload,headers={'X-CSRF-Token':self.customer_csrf})
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(r.json()['total'],396000)
        orders=self.customer.get('/api/orders').json()
        order=next(o for o in orders if o['order_number']==r.json()['order_number'])
        self.assertEqual(order['items'][0]['price'],198000)
        self.assertEqual(order['items'][0]['quantity'],2)
        self.assertEqual(order['status'],'pending')
        admin_orders=self.admin.get('/api/admin/orders').json()
        self.assertTrue(any(x['id']==order['id'] for x in admin_orders))
        r=self.admin.put('/api/admin/orders/'+order['id'],json={'status':'confirmed'},headers={'X-CSRF-Token':self.admin_csrf})
        self.assertEqual(r.status_code,200,r.text)
        r=self.customer.post('/api/orders/'+order['id']+'/cancel',headers={'X-CSRF-Token':self.customer_csrf})
        self.assertEqual(r.status_code,409)
        r=self.admin.put('/api/admin/orders/'+order['id'],json={'status':'completed'},headers={'X-CSRF-Token':self.admin_csrf})
        self.assertEqual(r.status_code,200)
        stats=self.admin.get('/api/admin/stats').json()
        self.assertGreaterEqual(stats['completed_revenue'],396000)

    def test_coming_soon_cannot_be_ordered(self):
        payload={'customer_name':'Khach thu nghiem','phone':'0987654321',
                 'address':'Dia chi da cho phep','items':[{'book_id':'upcoming-logic','quantity':1}]}
        r=self.customer.post('/api/orders',json=payload,headers={'X-CSRF-Token':self.customer_csrf})
        self.assertEqual(r.status_code,409,r.text)
        books=self.customer.get('/api/books').json()
        b=next(x for x in books if x['id']=='upcoming-logic')
        self.assertEqual(b['price'],280000)
        self.assertEqual(b['status'],'coming_soon')
        self.assertFalse(b['in_stock'])

    def test_customer_cancel_pending(self):
        payload={'customer_name':'Khach thu nghiem','phone':'0987654321',
                 'address':'Dia chi da cho phep','items':[{'book_id':'math6','quantity':1}]}
        r=self.customer.post('/api/orders',json=payload,headers={'X-CSRF-Token':self.customer_csrf})
        self.assertEqual(r.status_code,200,r.text)
        order=next(o for o in self.customer.get('/api/orders').json() if o['order_number']==r.json()['order_number'])
        r=self.customer.post('/api/orders/'+order['id']+'/cancel',headers={'X-CSRF-Token':self.customer_csrf})
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(next(o for o in self.customer.get('/api/orders').json() if o['id']==order['id'])['status'],'cancelled')

if __name__=='__main__': unittest.main()
