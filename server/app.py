"""Math Book Store: authenticated inventory API. No payment/order processing."""
import hashlib, hmac, io, json, os, secrets, sqlite3, time
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from PIL import Image, UnidentifiedImageError

HERE = Path(__file__).resolve().parent
WEB = HERE / "web"
DATA = Path(os.getenv("MBS_DATA_DIR", str(HERE / "data")))
UPLOADS = DATA / "uploads"
DATA.mkdir(parents=True, exist_ok=True)
UPLOADS.mkdir(parents=True, exist_ok=True)
DB = DATA / "shop.sqlite3"
COOKIE = "mbs_session"
SESSION_TTL = 7 * 86400
CATEGORIES = {"Lớp 6","Lớp 7","Lớp 8","Lớp 9","Ôn thi lớp 10","Khác"}
app = FastAPI(title="Math Book Store", docs_url=None, redoc_url=None, openapi_url=None)
attempts = {}

@contextmanager
def database():
    con = sqlite3.connect(DB, timeout=15)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()

def pw_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 260000)
    return salt + ":" + digest.hex()

def verify(password, saved):
    try:
        salt, digest = saved.split(":", 1)
        return hmac.compare_digest(pw_hash(password, salt).split(":")[1], digest)
    except Exception:
        return False

def init_db():
    with database() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL, csrf TEXT NOT NULL, expires INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS books (id TEXT PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, price INTEGER, image TEXT NOT NULL, description TEXT NOT NULL DEFAULT '', label TEXT NOT NULL DEFAULT '', sortOrder INTEGER NOT NULL DEFAULT 100, in_stock INTEGER NOT NULL DEFAULT 1);
        """)
        if not db.execute("SELECT 1 FROM books LIMIT 1").fetchone():
            for book in json.loads((WEB / "catalog.json").read_text(encoding="utf-8")):
                db.execute("INSERT INTO books VALUES (?,?,?,?,?,?,?,?,?)", (book["id"],book["name"],book["category"],book.get("price"),book["image"],book.get("description",""),book.get("label",""),book.get("sortOrder",100),1))
        admin_user = os.getenv("MBS_ADMIN_USER", "").strip().lower()
        admin_password = os.getenv("MBS_ADMIN_PASSWORD", "")
        if admin_user and len(admin_password) >= 12:
            if not db.execute("SELECT 1 FROM users WHERE username=?", (admin_user,)).fetchone():
                db.execute("INSERT INTO users(username,password,role) VALUES (?,?,?)",(admin_user,pw_hash(admin_password),"admin"))

init_db()

def origin_check(request):
    origin = request.headers.get("origin")
    if origin:
        from urllib.parse import urlsplit
        target = urlsplit(origin)
        if target.netloc != request.headers.get("host") or target.scheme != request.url.scheme:
            raise HTTPException(403, "Origin không hợp lệ")

def session(request):
    raw = request.cookies.get(COOKIE, "")
    if not raw: return None
    with database() as db:
        row = db.execute("""SELECT s.csrf,s.expires,u.id,u.username,u.role FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=?""",(hashlib.sha256(raw.encode()).hexdigest(),)).fetchone()
        if row and row["expires"] > int(time.time()): return dict(row)
    return None

def require(request, admin=False, write=False):
    user = session(request)
    if not user: raise HTTPException(401, "Bạn cần đăng nhập")
    if admin and user["role"] != "admin": raise HTTPException(403,"Chỉ quản trị viên")
    if write:
        origin_check(request)
        if not hmac.compare_digest(request.headers.get("x-csrf-token",""),user["csrf"]):
            raise HTTPException(403,"CSRF token không hợp lệ")
    return user

class Login(BaseModel):
    username: str = Field(min_length=3, max_length=60)
    password: str = Field(min_length=8, max_length=128)

class Book(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    category: str
    price: int | None = Field(default=None, ge=0, le=100000000)
    image: str = Field(min_length=2,max_length=500)
    description: str = Field(default="",max_length=1200)
    label: str = Field(default="",max_length=80)
    in_stock: bool = True

def as_book(row):
    book = dict(row)
    book["in_stock"] = bool(book["in_stock"])
    return book

@app.get("/health")
def health():
    return {"status":"ok","project":"math-book-store","stage":"inventory-v0.4","api_ready":True}

@app.get("/api/books")
def books():
    with database() as db:
        return [as_book(x) for x in db.execute("SELECT * FROM books ORDER BY sortOrder, name").fetchall()]

@app.get("/api/me")
def me(request:Request):
    user=session(request)
    return {"authenticated":bool(user),"username":user["username"] if user else None,"role":user["role"] if user else None,"csrf":user["csrf"] if user else None}

@app.post("/api/register")
def register(body:Login, request:Request):
    origin_check(request)
    username=body.username.strip().lower()
    if not username.replace("_","").isalnum() or len(body.password)<10:
        raise HTTPException(400,"Tên đăng nhập hoặc mật khẩu không hợp lệ (mật khẩu từ 10 ký tự)")
    with database() as db:
        if db.execute("SELECT 1 FROM users WHERE username=?",(username,)).fetchone():
            raise HTTPException(409,"Tên đăng nhập đã tồn tại")
        db.execute("INSERT INTO users(username,password,role) VALUES (?,?,?)",(username,pw_hash(body.password),"customer"))
    return {"ok":True}

@app.post("/api/login")
def login(body:Login,request:Request):
    origin_check(request)
    key=request.client.host if request.client else "unknown"
    now=time.time()
    attempts[key]=[t for t in attempts.get(key,[]) if now-t<300]
    if len(attempts[key])>=10: raise HTTPException(429,"Thử lại sau vài phút")
    attempts[key].append(now)
    with database() as db:
        user=db.execute("SELECT * FROM users WHERE username=?",(body.username.strip().lower(),)).fetchone()
        if not user or not verify(body.password,user["password"]):
            raise HTTPException(401,"Sai tên đăng nhập hoặc mật khẩu")
        raw=secrets.token_urlsafe(32)
        csrf=secrets.token_urlsafe(24)
        db.execute("DELETE FROM sessions WHERE expires<?",(int(now),))
        db.execute("INSERT INTO sessions VALUES (?,?,?,?)",(hashlib.sha256(raw.encode()).hexdigest(),user["id"],csrf,int(now)+SESSION_TTL))
    response=JSONResponse({"ok":True,"username":user["username"],"role":user["role"],"csrf":csrf})
    response.set_cookie(COOKIE,raw,httponly=True,secure=os.getenv("MBS_SECURE_COOKIES","0")=="1",samesite="lax",max_age=SESSION_TTL,path="/")
    return response

@app.post("/api/logout")
def logout(request:Request):
    require(request,write=True)
    raw=request.cookies.get(COOKIE,"")
    with database() as db: db.execute("DELETE FROM sessions WHERE token_hash=?",(hashlib.sha256(raw.encode()).hexdigest(),))
    response=JSONResponse({"ok":True})
    response.delete_cookie(COOKIE,path="/")
    return response

def validate(book):
    if book.category not in CATEGORIES: raise HTTPException(400,"Danh mục không hợp lệ")
    if not (book.image.startswith("assets/books/") or book.image.startswith("/api/images/")):
        raise HTTPException(400,"Ảnh phải là ảnh trong thư viện hoặc ảnh đã tải lên")
    if ".." in book.image: raise HTTPException(400,"Đường dẫn ảnh không hợp lệ")

@app.post("/api/admin/books")
def add_book(body:Book,request:Request):
    require(request,admin=True,write=True);validate(body)
    book_id=uuid4().hex[:12]
    with database() as db:
        sort_order=db.execute("SELECT COALESCE(MAX(sortOrder),0)+1 FROM books").fetchone()[0]
        db.execute("INSERT INTO books VALUES (?,?,?,?,?,?,?,?,?)",(book_id,body.name,body.category,body.price,body.image,body.description,body.label,sort_order,int(body.in_stock)))
    return {"ok":True,"id":book_id}

@app.put("/api/admin/books/{book_id}")
def edit_book(book_id:str,body:Book,request:Request):
    require(request,admin=True,write=True);validate(body)
    with database() as db:
        if not db.execute("SELECT 1 FROM books WHERE id=?",(book_id,)).fetchone(): raise HTTPException(404,"Không tìm thấy sách")
        db.execute("UPDATE books SET name=?, category=?, price=?, image=?, description=?, label=?, in_stock=? WHERE id=?",(body.name,body.category,body.price,body.image,body.description,body.label,int(body.in_stock),book_id))
    return {"ok":True}

@app.delete("/api/admin/books/{book_id}")
def delete_book(book_id:str,request:Request):
    require(request,admin=True,write=True)
    with database() as db:
        db.execute("DELETE FROM books WHERE id=?",(book_id,))
    return {"ok":True}

@app.post("/api/admin/upload")
async def upload(request:Request,file:UploadFile=File(...)):
    require(request,admin=True,write=True)
    if file.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(415,"Chỉ hỗ trợ JPG, PNG, WebP")
    raw=await file.read(5*1024*1024+1)
    if len(raw)>5*1024*1024: raise HTTPException(413,"Ảnh tối đa 5 MB")
    try:
        with Image.open(io.BytesIO(raw)) as photo:
            photo.verify()
        with Image.open(io.BytesIO(raw)) as photo:
            if photo.width*photo.height>20000000: raise HTTPException(413,"Ảnh quá lớn")
            if photo.format not in {"JPEG","PNG","WEBP"}: raise HTTPException(415,"Định dạng ảnh không hỗ trợ")
            img=photo.convert("RGB")
            img.thumbnail((1600,1600))
            filename=uuid4().hex+".webp"
            img.save(UPLOADS/filename,"WEBP",quality=85,method=4)
    except (UnidentifiedImageError,OSError,ValueError):
        raise HTTPException(400,"Ảnh không hợp lệ")
    return {"url":"/api/images/"+filename}

@app.get("/api/images/{name}")
def image(name:str):
    if not name.endswith(".webp") or len(name)!=37 or any(c not in "0123456789abcdef" for c in name[:-5]):
        raise HTTPException(404,"Không tìm thấy ảnh")
    path=UPLOADS/name
    if not path.is_file(): raise HTTPException(404,"Không tìm thấy ảnh")
    return FileResponse(path,media_type="image/webp",headers={"Cache-Control":"public,max-age=31536000,immutable"})

app.mount("/", StaticFiles(directory=WEB,html=True),name="web")
