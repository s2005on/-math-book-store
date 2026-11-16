"""API integration checks for Math Book Store v0.4."""
import io
import unittest
from fastapi.testclient import TestClient
from PIL import Image
from server.app import app, database, pw_hash

class InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client=TestClient(app)
        with database() as db:
            db.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES (?,?,?)",
                       ("ci_admin",pw_hash("TestingPass!234"),"admin"))

    def test_catalog_and_health(self):
        self.assertEqual(self.client.get("/health").status_code,200)
        books=self.client.get("/api/books").json()
        self.assertTrue(any(x["id"]=="63de" for x in books))

    def test_unauthorized_writes_blocked(self):
        book={"name":"Kiểm thử sách","category":"Lớp 6","price":10000,"image":"assets/books/math6-set.webp"}
        self.assertEqual(self.client.post("/api/admin/books",json=book).status_code,401)

    def test_login_crud_and_upload(self):
        with TestClient(app) as client:
            response=client.post("/api/login",json={"username":"ci_admin","password":"TestingPass!234"})
            self.assertEqual(response.status_code,200)
            token=response.json()["csrf"]
            headers={"X-CSRF-Token":token}
            book={"name":"Sách kiểm thử","category":"Lớp 8","price":99000,
                  "image":"assets/books/math8-set.webp","description":"Test","label":"Test","in_stock":True}
            self.assertEqual(client.post("/api/admin/books",json=book).status_code,403)
            added=client.post("/api/admin/books",json=book,headers=headers)
            self.assertEqual(added.status_code,200,added.text)
            key=added.json()["id"]
            book["in_stock"]=False
            self.assertEqual(client.put("/api/admin/books/"+key,json=book,headers=headers).status_code,200)
            self.assertFalse(next(x for x in client.get("/api/books").json() if x["id"]==key)["in_stock"])
            photo=Image.new("RGB",(60,80),"blue")
            buf=io.BytesIO()
            photo.save(buf,format="PNG")
            r=client.post("/api/admin/upload",files={"file":("cover.png",buf.getvalue(),"image/png")},headers=headers)
            self.assertEqual(r.status_code,200,r.text)
            self.assertEqual(client.get(r.json()["url"]).status_code,200)
            self.assertEqual(client.delete("/api/admin/books/"+key,headers=headers).status_code,200)
            self.assertEqual(client.post("/api/logout",headers=headers).status_code,200)
            self.assertEqual(client.post("/api/admin/books",json=book,headers=headers).status_code,401)

if __name__=="__main__": unittest.main()
