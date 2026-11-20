"""LTD's Book Store v1.3.0 Artaka Edition: modern local-first book shop, CRM & operations.

Local-first teaching & showcase project with full cart, shipping rules, stock tracking,
customer profile auto-fill, verified reviews, coming-soon waitlist, and admin analytics.
"""
from __future__ import annotations

import csv
import hashlib
import hmac
import io
import json
import os
import re
import secrets
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

import pydantic
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field

_PYDANTIC_V2 = int(getattr(pydantic, '__version__', '2').split('.')[0]) >= 2


def _list_field(min_len: int, max_len: int):
    if _PYDANTIC_V2:
        return Field(min_length=min_len, max_length=max_len)
    return Field(min_items=min_len, max_items=max_len)


def _model_to_dict(model: BaseModel) -> dict:
    return model.model_dump() if hasattr(model, 'model_dump') else model.dict()


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / '.env')
WEB = ROOT / 'web'
DATA = Path(os.environ.get('MBS_DATA_DIR', str(ROOT / 'data'))).resolve()
UPLOADS = DATA / 'uploads'
UPLOADS.mkdir(parents=True, exist_ok=True)
DB = DATA / 'shop.sqlite3'
COOKIE = 'mbs_session'
SESSION_TTL = 7 * 86400
CATEGORIES = {'Lớp 6', 'Lớp 7', 'Lớp 8', 'Lớp 9', 'Ôn thi lớp 10', 'Khác'}
BOOK_STATUSES = {'available', 'sold_out', 'coming_soon'}
ORDER_STATUSES = {'pending', 'confirmed', 'shipping', 'completed', 'cancelled'}

PAYMENT_METHODS = {
    'cod': 'Thanh toán khi nhận hàng (COD)',
    'bank_qr': 'Chuyển khoản VietQR 24/7',
    'momo': 'Ví điện tử MoMo',
    'vnpay': 'Cổng VNPAY-QR / Thẻ',
}
app = FastAPI(title="LTD's Book Store v1.3.0 Artaka Edition", docs_url=None, redoc_url=None, openapi_url=None)
login_attempts: dict[str, list[float]] = {}


@contextmanager
def database():
    db = sqlite3.connect(DB, timeout=20)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def pw_hash(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 260000)
    return salt + ':' + digest.hex()


def verify(password: str, saved: str) -> bool:
    try:
        salt, digest = saved.split(':', 1)
        return hmac.compare_digest(pw_hash(password, salt).split(':')[1], digest)
    except (ValueError, TypeError):
        return False


def init_db():
    with database() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS seed_history (key TEXT PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS site_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin','customer')),
                full_name TEXT NOT NULL DEFAULT '',
                phone TEXT NOT NULL DEFAULT '',
                address TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                csrf TEXT NOT NULL,
                expires INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER,
                image TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                label TEXT NOT NULL DEFAULT '',
                sortOrder INTEGER NOT NULL DEFAULT 100,
                in_stock INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'available',
                stock_qty INTEGER NOT NULL DEFAULT 50
            );
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                order_number TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                subtotal INTEGER NOT NULL DEFAULT 0,
                shipping_fee INTEGER NOT NULL DEFAULT 0,
                total INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                payment_method TEXT NOT NULL DEFAULT 'cod',
                promo_code TEXT NOT NULL DEFAULT '',
                discount_amount INTEGER NOT NULL DEFAULT 0,
                tracking_code TEXT NOT NULL DEFAULT '',
                admin_note TEXT NOT NULL DEFAULT '',
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                book_id TEXT NOT NULL,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                image TEXT NOT NULL,
                FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                author_name TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                comment TEXT NOT NULL,
                verified_purchase INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                UNIQUE(book_id, user_id),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS waitlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL,
                book_name TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                notified INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                UNIQUE(book_id, phone)
            );
            CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id, created_at);
            CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
            CREATE INDEX IF NOT EXISTS idx_reviews_book ON reviews(book_id, created_at);
            CREATE INDEX IF NOT EXISTS idx_waitlist_book ON waitlist(book_id, created_at);
        ''')
        # Backward-compatible schema migrations
        user_columns = {row['name'] for row in db.execute('PRAGMA table_info(users)')}
        if 'full_name' not in user_columns:
            db.execute("ALTER TABLE users ADD COLUMN full_name TEXT NOT NULL DEFAULT ''")
        if 'phone' not in user_columns:
            db.execute("ALTER TABLE users ADD COLUMN phone TEXT NOT NULL DEFAULT ''")
        if 'address' not in user_columns:
            db.execute("ALTER TABLE users ADD COLUMN address TEXT NOT NULL DEFAULT ''")
        if 'created_at' not in user_columns:
            db.execute("ALTER TABLE users ADD COLUMN created_at TEXT NOT NULL DEFAULT ''")

        book_cols = {x['name'] for x in db.execute('PRAGMA table_info(books)')}
        if 'status' not in book_cols:
            db.execute("ALTER TABLE books ADD COLUMN status TEXT NOT NULL DEFAULT 'available'")
            db.execute("UPDATE books SET status='sold_out' WHERE in_stock=0")
        if 'stock_qty' not in book_cols:
            db.execute("ALTER TABLE books ADD COLUMN stock_qty INTEGER NOT NULL DEFAULT 50")
            db.execute("UPDATE books SET stock_qty=0 WHERE status!='available'")

        order_cols = {x['name'] for x in db.execute('PRAGMA table_info(orders)')}
        if 'payment_method' not in order_cols:
            db.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT NOT NULL DEFAULT 'cod'")
        if 'promo_code' not in order_cols:
            db.execute("ALTER TABLE orders ADD COLUMN promo_code TEXT NOT NULL DEFAULT ''")
        if 'discount_amount' not in order_cols:
            db.execute("ALTER TABLE orders ADD COLUMN discount_amount INTEGER NOT NULL DEFAULT 0")
        if 'subtotal' not in order_cols:
            db.execute("ALTER TABLE orders ADD COLUMN subtotal INTEGER NOT NULL DEFAULT 0")
            db.execute("UPDATE orders SET subtotal = total + discount_amount WHERE subtotal = 0")
        if 'shipping_fee' not in order_cols:
            db.execute("ALTER TABLE orders ADD COLUMN shipping_fee INTEGER NOT NULL DEFAULT 0")
        if 'tracking_code' not in order_cols:
            db.execute("ALTER TABLE orders ADD COLUMN tracking_code TEXT NOT NULL DEFAULT ''")
        if 'admin_note' not in order_cols:
            db.execute("ALTER TABLE orders ADD COLUMN admin_note TEXT NOT NULL DEFAULT ''")

        if not db.execute("SELECT 1 FROM seed_history WHERE key='catalog-v060'").fetchone():
            if not db.execute('SELECT 1 FROM books LIMIT 1').fetchone():
                for b in json.loads((WEB / 'catalog.json').read_text(encoding='utf-8')):
                    status = b.get('status', 'available' if b.get('in_stock', True) else 'sold_out')
                    stock_qty = int(b.get('stock_qty', 50 if status == 'available' else 0))
                    db.execute(
                        '''INSERT INTO books(id,name,category,price,image,description,label,sortOrder,in_stock,status,stock_qty)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                        (b['id'], b['name'], b['category'], b.get('price'), b['image'],
                         b.get('description', ''), b.get('label', ''), b.get('sortOrder', 100),
                         int(status == 'available'), status, stock_qty),
                    )
            else:
                paths = {
                    'entrance': 'assets/books/entrance-set.webp',
                    'upcoming-logic': 'assets/books/coming-soon-combinatorics.svg',
                }
                for book_id, old_path in paths.items():
                    new_path = 'assets/books/entrance-set.webp' if book_id == 'entrance' else 'assets/books/upcoming-logic.webp'
                    if old_path != new_path:
                        db.execute('UPDATE books SET image=? WHERE id=? AND image=?', (new_path, book_id, old_path))
                db.execute("UPDATE books SET price=280000 WHERE id='upcoming-logic' AND price IS NULL")
                for b in json.loads((WEB / 'catalog.json').read_text(encoding='utf-8')):
                    if b['id'] in ('hsg7',) and not db.execute('SELECT 1 FROM books WHERE id=?', (b['id'],)).fetchone():
                        db.execute(
                            '''INSERT INTO books(id,name,category,price,image,description,label,sortOrder,in_stock,status,stock_qty)
                               VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                            (b['id'], b['name'], b['category'], b['price'], b['image'], b['description'], b['label'], b['sortOrder'], 0, 'coming_soon', 0),
                        )
            db.execute("INSERT INTO seed_history(key) VALUES('catalog-v060')")

        admin_name = os.environ.get('MBS_ADMIN_USER', '').strip().lower()
        admin_pass = os.environ.get('MBS_ADMIN_PASSWORD', '')
        if admin_name and len(admin_pass) >= 12 and not db.execute('SELECT 1 FROM users WHERE username=?', (admin_name,)).fetchone():
            db.execute(
                'INSERT INTO users(username,password,role,created_at) VALUES(?,?,?,?)',
                (admin_name, pw_hash(admin_pass), 'admin', datetime.now(timezone.utc).isoformat(timespec='seconds')),
            )


init_db()


def origin_check(request: Request):
    origin = request.headers.get('origin')
    if origin:
        parsed = urlsplit(origin)
        if parsed.netloc != request.headers.get('host') or parsed.scheme not in ('http', 'https'):
            raise HTTPException(403, 'Origin không hợp lệ')


def session(request: Request):
    raw = request.cookies.get(COOKIE, '')
    if not raw:
        return None
    with database() as db:
        row = db.execute(
            '''SELECT u.id,u.username,u.role,u.full_name,u.phone,u.address,s.csrf,s.expires
               FROM sessions s JOIN users u ON s.user_id=u.id WHERE s.token_hash=?''',
            (hashlib.sha256(raw.encode()).hexdigest(),),
        ).fetchone()
        if row and row['expires'] > int(time.time()):
            return dict(row)
    return None


def require(request: Request, *, admin=False, write=False):
    user = session(request)
    if not user:
        raise HTTPException(401, 'Vui lòng đăng nhập để tiếp tục')
    if admin and user['role'] != 'admin':
        raise HTTPException(403, 'Chỉ tài khoản quản trị được thực hiện')
    if write:
        origin_check(request)
        if not hmac.compare_digest(request.headers.get('x-csrf-token', ''), user['csrf']):
            raise HTTPException(403, 'Mã bảo vệ phiên đăng nhập không hợp lệ')
    return user


class Login(BaseModel):
    username: str = Field(min_length=3, max_length=60)
    password: str = Field(min_length=8, max_length=128)


class Registration(BaseModel):
    username: str = Field(min_length=3, max_length=60)
    password: str = Field(min_length=10, max_length=128)
    full_name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=10, max_length=16)


class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=9, max_length=16)
    address: str = Field(default='', max_length=240)


class PasswordUpdate(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=10, max_length=128)


class Book(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    category: str
    price: int | None = Field(default=None, ge=0, le=100_000_000)
    image: str = Field(min_length=2, max_length=500)
    description: str = Field(default='', max_length=1200)
    label: str = Field(default='', max_length=80)
    status: str | None = None
    in_stock: bool = True
    stock_qty: int | None = Field(default=None, ge=0, le=100_000)
    sortOrder: int | None = Field(default=None, ge=0, le=10_000)


class OrderLine(BaseModel):
    book_id: str = Field(min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=99)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=9, max_length=16)
    address: str = Field(min_length=8, max_length=240)
    note: str = Field(default='', max_length=240)
    payment_method: str = Field(default='cod', max_length=24)
    promo_code: str = Field(default='', max_length=32)
    items: list[OrderLine] = _list_field(1, 30)


class OrderChange(BaseModel):
    status: str
    tracking_code: str | None = Field(default=None, max_length=80)
    admin_note: str | None = Field(default=None, max_length=240)


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=3, max_length=600)


class WaitlistCreate(BaseModel):
    book_id: str = Field(min_length=1, max_length=80)
    customer_name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=9, max_length=16)
    note: str = Field(default='', max_length=200)


DEFAULT_BANNER = {
    'announcement_text': "LTD's BOOK STORE · CHỌN SÁCH ĐÚNG, HỌC TẬP HIỆU QUẢ",
    'hero_eyebrow': 'CHỌN SÁCH ĐÚNG · HỌC TOÁN TỐT',
    'hero_title_line1': 'Mỗi trang sách,',
    'hero_title_highlight': 'mở một lối tư duy.',
    'hero_description': 'Sách bài tập, luyện thi và bồi dưỡng Toán được chọn lọc theo từng khối lớp. Tìm cuốn sách phù hợp nhất cho lộ trình học tập của bạn.',
    'hero_sticker_top': 'STUDY',
    'hero_sticker_bottom': 'SMART',
    'hero_note_title': 'Học chắc từng bước',
    'hero_note_sub': 'Vững kiến thức · Tự tin kỳ thi',
    'coming_soon_eyebrow': 'ĐÓN ĐẦU KIẾN THỨC',
    'coming_soon_title': 'Sách',
    'coming_soon_highlight': 'sắp ra mắt.',
    'coming_soon_description': 'Khám phá những đầu sách đang chuẩn bị phát hành. Đăng ký nhận thông báo ngay khi sách mở bán chính thức.',
}

DEFAULT_SITE_CONFIG = {
    'store_name': "LTD's Book Store",
    'store_tagline': 'Mở trang sách, mở lối tư duy',
    'contact_name': 'LTD Book Store',
    'contact_phone': '0888 686 868',
    'contact_note': 'Hỗ trợ chọn sách & đơn hàng: 8:00 – 21:00',
    'theme_preset': 'emerald',
    'show_advisor': True,
    'show_coming_soon': True,
    'enable_promos': False,
    'freeship_threshold': 200_000,
    'shipping_fee': 25_000,
    'enable_shipping_fee': False,
    'categories': ['Lớp 6', 'Lớp 7', 'Lớp 8', 'Lớp 9', 'Ôn thi lớp 10', 'Khác'],
    'promos': [],
}


def load_site_config(db) -> dict:
    row = db.execute("SELECT value FROM site_settings WHERE key='site_config'").fetchone()
    cfg = {**DEFAULT_SITE_CONFIG, 'categories': list(DEFAULT_SITE_CONFIG['categories']), 'promos': []}
    if row:
        try:
            saved = json.loads(row['value'])
            if isinstance(saved, dict):
                for k in ('store_name', 'store_tagline', 'contact_name', 'contact_phone', 'contact_note', 'theme_preset'):
                    if isinstance(saved.get(k), str) and saved[k].strip():
                        cfg[k] = saved[k].strip()[:120]
                for k in ('show_advisor', 'show_coming_soon', 'enable_promos', 'enable_shipping_fee'):
                    if isinstance(saved.get(k), bool):
                        cfg[k] = saved[k]
                for k in ('freeship_threshold', 'shipping_fee'):
                    if saved.get(k) is not None:
                        cfg[k] = max(0, min(10_000_000, int(saved[k] or 0)))
                if isinstance(saved.get('categories'), list):
                    cats = [str(c).strip()[:50] for c in saved['categories'] if str(c).strip()]
                    if cats:
                        cfg['categories'] = cats
                if isinstance(saved.get('promos'), list):
                    clean_promos = []
                    for pr in saved['promos']:
                        if not isinstance(pr, dict):
                            continue
                        code = str(pr.get('code', '')).strip().upper()[:24]
                        if not code:
                            continue
                        ptype = pr.get('type') if pr.get('type') in ('percent', 'fixed') else 'fixed'
                        val = max(1, min(10_000_000, int(pr.get('value', 0) or 0)))
                        min_order = max(0, min(100_000_000, int(pr.get('min_order', 0) or 0)))
                        max_discount = max(0, min(10_000_000, int(pr.get('max_discount', 0) or 0)))
                        clean_promos.append({
                            'code': code,
                            'type': ptype,
                            'value': val,
                            'min_order': min_order,
                            'max_discount': max_discount,
                            'active': bool(pr.get('active', True)),
                            'show_public': bool(pr.get('show_public', False)),
                            'label': str(pr.get('label', '')).strip()[:60],
                        })
                    cfg['promos'] = clean_promos
        except Exception:
            pass
    return cfg


def compute_shipping(subtotal: int, cfg: dict) -> int:
    if not cfg.get('enable_shipping_fee'):
        return 0
    threshold = int(cfg.get('freeship_threshold', 200_000) or 0)
    fee = int(cfg.get('shipping_fee', 25_000) or 0)
    if subtotal <= 0 or (threshold > 0 and subtotal >= threshold):
        return 0
    return fee


class BannerConfig(BaseModel):
    announcement_text: str = Field(min_length=2, max_length=180)
    hero_eyebrow: str = Field(min_length=2, max_length=100)
    hero_title_line1: str = Field(min_length=2, max_length=100)
    hero_title_highlight: str = Field(min_length=2, max_length=100)
    hero_description: str = Field(min_length=5, max_length=400)
    hero_sticker_top: str = Field(min_length=1, max_length=20)
    hero_sticker_bottom: str = Field(min_length=1, max_length=20)
    hero_note_title: str = Field(min_length=2, max_length=80)
    hero_note_sub: str = Field(min_length=2, max_length=100)
    coming_soon_eyebrow: str = Field(min_length=2, max_length=100)
    coming_soon_title: str = Field(min_length=1, max_length=60)
    coming_soon_highlight: str = Field(min_length=1, max_length=60)
    coming_soon_description: str = Field(min_length=5, max_length=400)


def status_of(book: Book) -> str:
    if book.status:
        if book.status == 'available' and book.stock_qty is not None and book.stock_qty <= 0:
            return 'sold_out'
        return book.status
    if not book.in_stock or (book.stock_qty is not None and book.stock_qty <= 0):
        return 'sold_out'
    return 'available'


def as_book(row, rating_map=None, waitlist_map=None):
    item = dict(row)
    qty = int(item.get('stock_qty') if item.get('stock_qty') is not None else (50 if item['status'] == 'available' else 0))
    item['stock_qty'] = qty
    item['in_stock'] = item['status'] == 'available' and qty > 0
    if rating_map and item['id'] in rating_map:
        r_avg, r_cnt = rating_map[item['id']]
        item['rating_avg'] = round(r_avg, 1)
        item['review_count'] = r_cnt
    else:
        item['rating_avg'] = 0.0
        item['review_count'] = 0
    item['waitlist_count'] = (waitlist_map or {}).get(item['id'], 0)
    return item


def get_orders(db, where='', args=()):
    query = 'SELECT * FROM orders ' + where + ' ORDER BY created_at DESC, rowid DESC'
    result = []
    for row in db.execute(query, args).fetchall():
        order = dict(row)
        order['payment_label'] = PAYMENT_METHODS.get(order.get('payment_method', 'cod'), 'Thanh toán COD')
        order['items'] = [
            dict(item)
            for item in db.execute(
                '''SELECT book_id,name,price,quantity,image FROM order_items
                   WHERE order_id=? ORDER BY id''',
                (order['id'],),
            ).fetchall()
        ]
        result.append(order)
    return result


@app.get('/health')
def health():
    return {
        'status': 'ok',
        'project': 'ltds-book-store',
        'stage': 'art-edition-v1.2.1',
        'version': '1.3.0',
        'api_ready': True,
    }


@app.get('/api/books')
def books():
    with database() as db:
        rating_rows = db.execute('SELECT book_id, AVG(rating) AS avg_r, COUNT(*) AS cnt FROM reviews GROUP BY book_id').fetchall()
        rating_map = {r['book_id']: (float(r['avg_r']), int(r['cnt'])) for r in rating_rows}
        wait_rows = db.execute('SELECT book_id, COUNT(*) AS cnt FROM waitlist GROUP BY book_id').fetchall()
        wait_map = {w['book_id']: int(w['cnt']) for w in wait_rows}
        return [as_book(b, rating_map, wait_map) for b in db.execute('SELECT * FROM books ORDER BY sortOrder,name').fetchall()]


@app.get('/api/books/{book_id}/reviews')
def get_book_reviews(book_id: str):
    with database() as db:
        rows = db.execute(
            '''SELECT id, book_id, author_name, rating, comment, verified_purchase, created_at
               FROM reviews WHERE book_id=? ORDER BY created_at DESC, id DESC LIMIT 50''',
            (book_id,),
        ).fetchall()
        return [dict(r) for r in rows]


@app.post('/api/books/{book_id}/reviews')
def add_book_review(book_id: str, body: ReviewCreate, request: Request):
    user = require(request, write=True)
    comment = ' '.join(body.comment.strip().split())
    if len(comment) < 3:
        raise HTTPException(400, 'Nhận xét cần tối thiểu 3 ký tự')
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    with database() as db:
        book = db.execute('SELECT id FROM books WHERE id=?', (book_id,)).fetchone()
        if not book:
            raise HTTPException(404, 'Không tìm thấy đầu sách')
        bought = db.execute(
            '''SELECT 1 FROM orders o JOIN order_items oi ON o.id = oi.order_id
               WHERE o.user_id=? AND oi.book_id=? AND o.status != 'cancelled' LIMIT 1''',
            (user['id'], book_id),
        ).fetchone()
        author = (user.get('full_name') or '').strip() or user['username']
        db.execute(
            '''INSERT INTO reviews(book_id, user_id, author_name, rating, comment, verified_purchase, created_at)
               VALUES(?,?,?,?,?,?,?)
               ON CONFLICT(book_id, user_id) DO UPDATE SET
                 author_name=excluded.author_name,
                 rating=excluded.rating,
                 comment=excluded.comment,
                 verified_purchase=excluded.verified_purchase,
                 created_at=excluded.created_at''',
            (book_id, user['id'], author, int(body.rating), comment, int(bool(bought)), now),
        )
    return {'ok': True}


@app.post('/api/waitlist')
def join_waitlist(body: WaitlistCreate, request: Request):
    origin_check(request)
    phone = re.sub(r'[ .-]', '', body.phone.strip())
    if not re.fullmatch(r'0[35789][0-9]{8}', phone):
        raise HTTPException(400, 'Số điện thoại nhận thông báo phải gồm 10 số hợp lệ (03, 05, 07, 08, 09)')
    clean_name = ' '.join(body.customer_name.strip().split())
    if len(clean_name) < 2:
        raise HTTPException(400, 'Vui lòng nhập họ tên hợp lệ')
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    with database() as db:
        book = db.execute('SELECT id, name, status FROM books WHERE id=?', (body.book_id,)).fetchone()
        if not book:
            raise HTTPException(404, 'Không tìm thấy đầu sách')
        db.execute(
            '''INSERT INTO waitlist(book_id, book_name, customer_name, phone, note, notified, created_at)
               VALUES(?,?,?,?,?,0,?)
               ON CONFLICT(book_id, phone) DO UPDATE SET
                 customer_name=excluded.customer_name,
                 note=excluded.note,
                 created_at=excluded.created_at''',
            (book['id'], book['name'], clean_name, phone, body.note.strip(), now),
        )
        cnt = db.execute('SELECT COUNT(*) FROM waitlist WHERE book_id=?', (book['id'],)).fetchone()[0]
    return {'ok': True, 'waitlist_count': cnt, 'message': f'Đã đăng ký nhận thông báo khi "{book["name"]}" mở bán!'}


@app.get('/api/me')
def me(request: Request):
    u = session(request)
    if not u:
        return {'authenticated': False, 'username': None, 'role': None, 'csrf': None}
    saved_address = u.get('address') or ''
    if not saved_address:
        with database() as db:
            last_order = db.execute(
                'SELECT address FROM orders WHERE user_id=? ORDER BY created_at DESC LIMIT 1',
                (u['id'],),
            ).fetchone()
            if last_order:
                saved_address = last_order['address']
    return {
        'authenticated': True,
        'username': u['username'],
        'role': u['role'],
        'csrf': u['csrf'],
        'full_name': u.get('full_name') or '',
        'phone': u.get('phone') or '',
        'address': saved_address,
    }


@app.put('/api/me/profile')
def update_my_profile(body: ProfileUpdate, request: Request):
    user = require(request, write=True)
    full_name = ' '.join(body.full_name.strip().split())
    phone = re.sub(r'[ .-]', '', body.phone.strip())
    address = ' '.join(body.address.strip().split())
    if len(full_name) < 2:
        raise HTTPException(400, 'Họ và tên phải có ít nhất 2 ký tự')
    if not re.fullmatch(r'0[35789][0-9]{8}', phone):
        raise HTTPException(400, 'Số điện thoại Việt Nam phải có 10 chữ số (03, 05, 07, 08, 09)')
    with database() as db:
        db.execute(
            'UPDATE users SET full_name=?, phone=?, address=? WHERE id=?',
            (full_name, phone, address, user['id']),
        )
    return {'ok': True, 'full_name': full_name, 'phone': phone, 'address': address}


@app.post('/api/me/password')
def change_my_password(body: PasswordUpdate, request: Request):
    user = require(request, write=True)
    with database() as db:
        row = db.execute('SELECT password FROM users WHERE id=?', (user['id'],)).fetchone()
        if not row or not verify(body.current_password, row['password']):
            raise HTTPException(400, 'Mật khẩu hiện tại không chính xác')
        db.execute('UPDATE users SET password=? WHERE id=?', (pw_hash(body.new_password), user['id']))
    return {'ok': True}


@app.post('/api/register')
def register(body: Registration, request: Request):
    origin_check(request)
    username = body.username.strip().lower()
    full_name = ' '.join(body.full_name.split())
    phone = re.sub(r'[ .-]', '', body.phone.strip())
    if not re.fullmatch(r'[a-z0-9_]{3,60}', username):
        raise HTTPException(400, 'Tên đăng nhập phải gồm 3–60 ký tự a-z, 0-9 hoặc _')
    if len(full_name) < 2 or len(full_name) > 80 or any(ord(ch) < 32 for ch in full_name):
        raise HTTPException(400, 'Vui lòng nhập họ và tên hợp lệ')
    if not re.fullmatch(r'0[35789][0-9]{8}', phone):
        raise HTTPException(400, 'Số điện thoại phải có 10 chữ số và bắt đầu bằng 03, 05, 07, 08 hoặc 09')
    now_iso = datetime.now(timezone.utc).isoformat(timespec='seconds')
    with database() as db:
        if db.execute('SELECT 1 FROM users WHERE username=?', (username,)).fetchone():
            raise HTTPException(409, 'Tên đăng nhập đã tồn tại')
        db.execute(
            'INSERT INTO users(username,password,role,full_name,phone,created_at) VALUES (?,?,?,?,?,?)',
            (username, pw_hash(body.password), 'customer', full_name, phone, now_iso),
        )
    return {'ok': True}


@app.post('/api/login')
def login(body: Login, request: Request):
    origin_check(request)
    key = request.client.host if request.client else 'local'
    now = time.time()
    login_attempts[key] = [v for v in login_attempts.get(key, []) if now - v < 300]
    if len(login_attempts[key]) >= 15:
        raise HTTPException(429, 'Đã thử đăng nhập quá nhiều lần, vui lòng thử lại sau')
    login_attempts[key].append(now)
    with database() as db:
        user = db.execute('SELECT * FROM users WHERE username=?', (body.username.strip().lower(),)).fetchone()
        if not user or not verify(body.password, user['password']):
            raise HTTPException(401, 'Sai tên đăng nhập hoặc mật khẩu')
        token = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(24)
        db.execute('DELETE FROM sessions WHERE expires<?', (int(now),))
        db.execute(
            'INSERT INTO sessions VALUES(?,?,?,?)',
            (hashlib.sha256(token.encode()).hexdigest(), user['id'], csrf, int(now) + SESSION_TTL),
        )
    response = JSONResponse({'ok': True, 'username': user['username'], 'role': user['role'], 'csrf': csrf})
    response.set_cookie(
        COOKIE,
        token,
        httponly=True,
        secure=os.getenv('MBS_SECURE_COOKIES', '0') == '1',
        samesite='lax',
        max_age=SESSION_TTL,
        path='/',
    )
    return response


@app.post('/api/logout')
def logout(request: Request):
    require(request, write=True)
    raw = request.cookies.get(COOKIE, '')
    with database() as db:
        db.execute('DELETE FROM sessions WHERE token_hash=?', (hashlib.sha256(raw.encode()).hexdigest(),))
    response = JSONResponse({'ok': True})
    response.delete_cookie(COOKIE, path='/')
    return response


def validate_book(book: Book):
    cat = book.category.strip()
    if not cat or len(cat) > 50:
        raise HTTPException(400, 'Danh mục không hợp lệ')
    if status_of(book) not in BOOK_STATUSES:
        raise HTTPException(400, 'Trạng thái không hợp lệ')
    if '..' in book.image or not (book.image.startswith('assets/books/') or book.image.startswith('/api/images/')):
        raise HTTPException(400, 'Vui lòng dùng ảnh trong thư viện hoặc ảnh đã tải lên')
    if book.image.startswith('assets/books/') and not (WEB / book.image).is_file():
        raise HTTPException(400, 'Ảnh không tồn tại trên máy chủ')
    if book.image.startswith('/api/images/') and not (UPLOADS / Path(book.image).name).is_file():
        raise HTTPException(400, 'Ảnh chưa được tải lên')


@app.get('/api/admin/library-images')
def list_library_images(request: Request):
    require(request, admin=True)
    builtin = sorted(
        f'assets/books/{p.name}'
        for p in (WEB / 'assets/books').glob('*')
        if p.suffix.lower() in {'.webp', '.png', '.jpg', '.jpeg', '.svg'}
    )
    uploaded = sorted(
        f'/api/images/{p.name}'
        for p in UPLOADS.glob('*.webp')
    )
    return {'builtin': builtin, 'uploaded': uploaded}


@app.post('/api/admin/books')
def add_book(body: Book, request: Request):
    require(request, admin=True, write=True)
    validate_book(body)
    status = status_of(body)
    stock_qty = int(body.stock_qty if body.stock_qty is not None else (50 if status == 'available' else 0))
    if status != 'available':
        stock_qty = 0 if status == 'sold_out' else stock_qty
    uid = uuid4().hex[:12]
    with database() as db:
        order = body.sortOrder if body.sortOrder is not None else db.execute('SELECT COALESCE(MAX(sortOrder),0)+1 FROM books').fetchone()[0]
        db.execute(
            '''INSERT INTO books(id,name,category,price,image,description,label,sortOrder,in_stock,status,stock_qty)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
            (uid, body.name.strip(), body.category.strip(), body.price, body.image, body.description, body.label,
             order, int(status == 'available' and stock_qty > 0), status, stock_qty),
        )
    return {'ok': True, 'id': uid}


@app.put('/api/admin/books/{book_id}')
def edit_book(book_id: str, body: Book, request: Request):
    require(request, admin=True, write=True)
    validate_book(body)
    status = status_of(body)
    with database() as db:
        existing = db.execute('SELECT sortOrder, stock_qty FROM books WHERE id=?', (book_id,)).fetchone()
        if not existing:
            raise HTTPException(404, 'Không tìm thấy sách')
        if body.stock_qty is not None:
            stock_qty = int(body.stock_qty)
        else:
            stock_qty = (max(1, int(existing['stock_qty'] or 50)) if status == 'available' else 0)
        if status == 'sold_out':
            stock_qty = 0
        sort_order = body.sortOrder if body.sortOrder is not None else existing['sortOrder']
        db.execute(
            '''UPDATE books SET name=?,category=?,price=?,image=?,description=?,label=?,
               sortOrder=?,in_stock=?,status=?,stock_qty=? WHERE id=?''',
            (body.name.strip(), body.category.strip(), body.price, body.image, body.description, body.label,
             sort_order, int(status == 'available' and stock_qty > 0), status, stock_qty, book_id),
        )
    return {'ok': True}


@app.delete('/api/admin/books/{book_id}')
def delete_book(book_id: str, request: Request):
    require(request, admin=True, write=True)
    with database() as db:
        result = db.execute('DELETE FROM books WHERE id=?', (book_id,))
        if not result.rowcount:
            raise HTTPException(404, 'Không tìm thấy sách')
    return {'ok': True}


@app.post('/api/admin/upload')
async def upload(request: Request, file: UploadFile = File(...)):
    require(request, admin=True, write=True)
    if file.content_type not in {'image/jpeg', 'image/png', 'image/webp'}:
        raise HTTPException(415, 'Chỉ hỗ trợ ảnh JPG, PNG hoặc WebP')
    raw = await file.read(5 * 1024 * 1024 + 1)
    if len(raw) > 5 * 1024 * 1024:
        raise HTTPException(413, 'Ảnh tối đa 5MB')
    try:
        with Image.open(io.BytesIO(raw)) as photo:
            photo.verify()
        with Image.open(io.BytesIO(raw)) as photo:
            if photo.width * photo.height > 20_000_000:
                raise HTTPException(413, 'Ảnh có kích thước quá lớn')
            if photo.format not in {'JPEG', 'PNG', 'WEBP'}:
                raise HTTPException(415, 'Tệp không phải định dạng ảnh hợp lệ')
            image = photo.convert('RGB')
            image.thumbnail((1800, 1800))
            filename = uuid4().hex + '.webp'
            image.save(UPLOADS / filename, 'WEBP', quality=91, method=5)
    except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError):
        raise HTTPException(400, 'Không đọc được ảnh; vui lòng chọn ảnh hợp lệ')
    return {'url': '/api/images/' + filename}


@app.get('/api/images/{name}')
def image(name: str):
    if not re.fullmatch(r'[0-9a-f]{32}\.webp', name):
        raise HTTPException(404, 'Không tìm thấy ảnh')
    path = UPLOADS / name
    if not path.is_file():
        raise HTTPException(404, 'Không tìm thấy ảnh')
    return FileResponse(path, media_type='image/webp', headers={'Cache-Control': 'public,max-age=31536000,immutable'})


@app.post('/api/orders')
def place_order(body: OrderCreate, request: Request):
    user = require(request, write=True)
    if not re.fullmatch(r'[0-9+().\s-]{9,16}', body.phone) or len(re.sub(r'\D', '', body.phone)) not in (9, 10, 11):
        raise HTTPException(400, 'Số điện thoại không hợp lệ')
    if len(body.customer_name.strip()) < 2 or len(body.address.strip()) < 8:
        raise HTTPException(400, 'Vui lòng nhập đầy đủ họ tên và địa chỉ')
    quantities: dict[str, int] = {}
    for line in body.items:
        quantities[line.book_id] = quantities.get(line.book_id, 0) + line.quantity
        if quantities[line.book_id] > 99:
            raise HTTPException(400, 'Số lượng sách vượt giới hạn')
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    order_id = uuid4().hex
    order_code = 'LTD-' + datetime.now(timezone.utc).strftime('%y%m%d') + '-' + secrets.token_hex(3).upper()
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        cfg = load_site_config(db)
        snapshots = []
        subtotal = 0
        for book_id, quantity in quantities.items():
            book = db.execute('SELECT * FROM books WHERE id=?', (book_id,)).fetchone()
            if not book or book['status'] != 'available' or book['price'] is None:
                raise HTTPException(409, 'Một số sách không còn được bán; hãy cập nhật lại giỏ hàng')
            avail_qty = int(book['stock_qty'] if book['stock_qty'] is not None else 50)
            if avail_qty < quantity:
                raise HTTPException(409, f'Sách "{book["name"]}" hiện chỉ còn {avail_qty} cuốn trong kho')
            line_total = book['price'] * quantity
            subtotal += line_total
            snapshots.append((order_id, book_id, book['name'], book['price'], quantity, book['image']))
        if subtotal > 100_000_000:
            raise HTTPException(400, 'Đơn hàng vượt giới hạn')
        pm = body.payment_method.strip().lower() or 'cod'
        if pm not in PAYMENT_METHODS:
            raise HTTPException(400, 'Phương thức thanh toán không hợp lệ')
        code = body.promo_code.strip().upper()
        discount = 0
        if code:
            if not cfg.get('enable_promos'):
                raise HTTPException(400, 'Hiện tại cửa hàng chưa mở chương trình mã giảm giá')
            matched = next((pr for pr in cfg['promos'] if pr['code'] == code and pr['active']), None)
            if not matched:
                raise HTTPException(400, 'Mã giảm giá không hợp lệ hoặc đã ngừng áp dụng')
            if subtotal < matched['min_order']:
                raise HTTPException(400, f"Mã {code} áp dụng cho đơn từ {matched['min_order']:,}đ".replace(',', '.'))
            if matched['type'] == 'percent':
                discount = round(subtotal * matched['value'] / 100)
                if matched['max_discount'] > 0:
                    discount = min(discount, matched['max_discount'])
            else:
                discount = matched['value']
            discount = min(subtotal, max(0, discount))
        shipping_fee = compute_shipping(subtotal, cfg)
        final_total = max(0, subtotal - discount + shipping_fee)

        # Deduct stock quantities cleanly
        for book_id, quantity in quantities.items():
            row_b = db.execute('SELECT stock_qty FROM books WHERE id=?', (book_id,)).fetchone()
            new_qty = max(0, int(row_b['stock_qty'] or 0) - quantity)
            new_status = 'available' if new_qty > 0 else 'sold_out'
            db.execute(
                'UPDATE books SET stock_qty=?, in_stock=?, status=? WHERE id=?',
                (new_qty, int(new_qty > 0), new_status, book_id),
            )

        # Save default delivery address on user profile if empty
        db.execute(
            '''UPDATE users SET
                 full_name = CASE WHEN full_name = '' THEN ? ELSE full_name END,
                 phone = CASE WHEN phone = '' THEN ? ELSE phone END,
                 address = ?
               WHERE id=?''',
            (body.customer_name.strip(), re.sub(r'[ .-]', '', body.phone.strip()), body.address.strip(), user['id']),
        )

        db.execute(
            '''INSERT INTO orders(id,order_number,user_id,customer_name,phone,address,note,subtotal,shipping_fee,total,status,created_at,updated_at,payment_method,promo_code,discount_amount)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (order_id, order_code, user['id'], body.customer_name.strip(), body.phone.strip(),
             body.address.strip(), body.note.strip(), subtotal, shipping_fee, final_total, 'pending', now, now, pm, code, discount),
        )
        db.executemany(
            '''INSERT INTO order_items(order_id,book_id,name,price,quantity,image)
               VALUES(?,?,?,?,?,?)''',
            snapshots,
        )
    return {
        'ok': True,
        'order_number': order_code,
        'total': final_total,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'discount_amount': discount,
        'promo_code': code,
        'payment_method': pm,
        'payment_label': PAYMENT_METHODS[pm],
        'status': 'pending',
    }


def _restore_order_stock(db, order_id: str):
    items = db.execute('SELECT book_id, quantity FROM order_items WHERE order_id=?', (order_id,)).fetchall()
    for it in items:
        bk = db.execute('SELECT stock_qty, status FROM books WHERE id=?', (it['book_id'],)).fetchone()
        if bk and bk['status'] != 'coming_soon':
            restored = int(bk['stock_qty'] or 0) + int(it['quantity'])
            db.execute(
                "UPDATE books SET stock_qty=?, in_stock=1, status='available' WHERE id=?",
                (restored, it['book_id']),
            )


@app.get('/api/orders')
def my_orders(request: Request):
    user = require(request)
    with database() as db:
        return get_orders(db, 'WHERE user_id=?', (user['id'],))


@app.post('/api/orders/{order_id}/cancel')
def cancel_order(order_id: str, request: Request):
    user = require(request, write=True)
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        order = db.execute('SELECT id,status FROM orders WHERE id=? AND user_id=?', (order_id, user['id'])).fetchone()
        if not order:
            raise HTTPException(404, 'Không tìm thấy đơn hàng')
        if order['status'] != 'pending':
            raise HTTPException(409, 'Đơn hàng đã được xử lý, không thể tự hủy')
        _restore_order_stock(db, order_id)
        db.execute(
            'UPDATE orders SET status=?,updated_at=? WHERE id=?',
            ('cancelled', datetime.now(timezone.utc).isoformat(timespec='seconds'), order_id),
        )
    return {'ok': True}


@app.get('/api/admin/orders')
def admin_orders(request: Request):
    require(request, admin=True)
    with database() as db:
        return get_orders(db)


@app.get('/api/admin/orders/export.csv')
def export_orders_csv(request: Request):
    require(request, admin=True)
    with database() as db:
        orders = get_orders(db)
    buf = io.StringIO()
    buf.write('\ufeff')
    writer = csv.writer(buf)
    writer.writerow([
        'Mã đơn', 'Ngày tạo', 'Khách hàng', 'Số điện thoại', 'Địa chỉ',
        'Sản phẩm', 'Tạm tính', 'Giảm giá', 'Phí vận chuyển', 'Tổng thanh toán',
        'Thanh toán', 'Trạng thái', 'Mã vận đơn', 'Ghi chú khách', 'Ghi chú shop',
    ])
    for o in orders:
        items_str = '; '.join(f"{i['name']} x{i['quantity']}" for i in o['items'])
        writer.writerow([
            o['order_number'], o['created_at'], o['customer_name'], o['phone'], o['address'],
            items_str, o.get('subtotal', o['total']), o.get('discount_amount', 0), o.get('shipping_fee', 0), o['total'],
            o.get('payment_label', o.get('payment_method', 'cod')), o['status'],
            o.get('tracking_code', ''), o.get('note', ''), o.get('admin_note', ''),
        ])
    return Response(
        content=buf.getvalue().encode('utf-8'),
        media_type='text/csv; charset=utf-8',
        headers={'Content-Disposition': 'attachment; filename="ltds-orders-report.csv"'},
    )


@app.put('/api/admin/orders/{order_id}')
def change_order(order_id: str, body: OrderChange, request: Request):
    require(request, admin=True, write=True)
    if body.status not in ORDER_STATUSES:
        raise HTTPException(400, 'Trạng thái đơn hàng không hợp lệ')
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        previous = db.execute('SELECT status, tracking_code, admin_note FROM orders WHERE id=?', (order_id,)).fetchone()
        if not previous:
            raise HTTPException(404, 'Không tìm thấy đơn hàng')
        if previous['status'] in ('completed', 'cancelled') and previous['status'] != body.status:
            raise HTTPException(409, 'Không thể sửa đơn hàng đã hoàn tất hoặc đã hủy')
        if body.status == 'cancelled' and previous['status'] != 'cancelled':
            _restore_order_stock(db, order_id)
        tracking = body.tracking_code.strip() if body.tracking_code is not None else (previous['tracking_code'] or '')
        adm_note = body.admin_note.strip() if body.admin_note is not None else (previous['admin_note'] or '')
        db.execute(
            'UPDATE orders SET status=?, tracking_code=?, admin_note=?, updated_at=? WHERE id=?',
            (body.status, tracking, adm_note, datetime.now(timezone.utc).isoformat(timespec='seconds'), order_id),
        )
    return {'ok': True}


@app.get('/api/admin/customers')
def admin_customers(request: Request):
    require(request, admin=True)
    with database() as db:
        rows = db.execute(
            '''SELECT u.id, u.username, u.full_name, u.phone, u.address, u.created_at,
                      COUNT(o.id) AS order_count,
                      COALESCE(SUM(CASE WHEN o.status != 'cancelled' THEN o.total ELSE 0 END), 0) AS total_spent
               FROM users u
               LEFT JOIN orders o ON u.id = o.user_id
               WHERE u.role = 'customer'
               GROUP BY u.id
               ORDER BY total_spent DESC, u.id DESC'''
        ).fetchall()
        return [dict(r) for r in rows]


@app.get('/api/admin/waitlist')
def admin_waitlist(request: Request):
    require(request, admin=True)
    with database() as db:
        rows = db.execute('SELECT * FROM waitlist ORDER BY notified ASC, created_at DESC').fetchall()
        return [dict(r) for r in rows]


@app.put('/api/admin/waitlist/{entry_id}')
def mark_waitlist_notified(entry_id: int, body: dict, request: Request):
    require(request, admin=True, write=True)
    notified = int(bool((body or {}).get('notified', True)))
    with database() as db:
        res = db.execute('UPDATE waitlist SET notified=? WHERE id=?', (notified, entry_id))
        if not res.rowcount:
            raise HTTPException(404, 'Không tìm thấy đăng ký chờ sách')
    return {'ok': True}


@app.delete('/api/admin/waitlist/{entry_id}')
def delete_waitlist_entry(entry_id: int, request: Request):
    require(request, admin=True, write=True)
    with database() as db:
        db.execute('DELETE FROM waitlist WHERE id=?', (entry_id,))
    return {'ok': True}


@app.get('/api/admin/reviews')
def admin_reviews(request: Request):
    require(request, admin=True)
    with database() as db:
        rows = db.execute(
            '''SELECT r.*, b.name AS book_name
               FROM reviews r LEFT JOIN books b ON r.book_id = b.id
               ORDER BY r.created_at DESC'''
        ).fetchall()
        return [dict(r) for r in rows]


@app.delete('/api/admin/reviews/{review_id}')
def admin_delete_review(review_id: int, request: Request):
    require(request, admin=True, write=True)
    with database() as db:
        db.execute('DELETE FROM reviews WHERE id=?', (review_id,))
    return {'ok': True}


@app.get('/api/admin/stats')
def admin_stats(request: Request):
    require(request, admin=True)
    with database() as db:
        top_books = [
            dict(r)
            for r in db.execute(
                '''SELECT oi.book_id, oi.name, SUM(oi.quantity) AS sold_qty, SUM(oi.price * oi.quantity) AS revenue
                   FROM order_items oi
                   JOIN orders o ON o.id = oi.order_id
                   WHERE o.status != 'cancelled'
                   GROUP BY oi.book_id, oi.name
                   ORDER BY sold_qty DESC, revenue DESC
                   LIMIT 5'''
            ).fetchall()
        ]
        by_payment = [
            dict(r)
            for r in db.execute(
                '''SELECT payment_method, COUNT(*) AS count, COALESCE(SUM(total), 0) AS revenue
                   FROM orders WHERE status != 'cancelled'
                   GROUP BY payment_method'''
            ).fetchall()
        ]
        return {
            'books': db.execute('SELECT COUNT(*) FROM books').fetchone()[0],
            'coming_soon': db.execute("SELECT COUNT(*) FROM books WHERE status='coming_soon'").fetchone()[0],
            'low_stock': db.execute("SELECT COUNT(*) FROM books WHERE status='available' AND stock_qty <= 5").fetchone()[0],
            'orders': db.execute('SELECT COUNT(*) FROM orders').fetchone()[0],
            'pending': db.execute("SELECT COUNT(*) FROM orders WHERE status='pending'").fetchone()[0],
            'shipping': db.execute("SELECT COUNT(*) FROM orders WHERE status='shipping'").fetchone()[0],
            'completed_revenue': db.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE status='completed'").fetchone()[0],
            'active_revenue': db.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE status IN ('pending','confirmed','shipping','completed')").fetchone()[0],
            'customers': db.execute("SELECT COUNT(*) FROM users WHERE role='customer'").fetchone()[0],
            'waitlist_count': db.execute('SELECT COUNT(*) FROM waitlist WHERE notified=0').fetchone()[0],
            'reviews_count': db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0],
            'top_books': top_books,
            'by_payment': by_payment,
        }


@app.get('/api/banner')
def get_banner():
    with database() as db:
        row = db.execute("SELECT value FROM site_settings WHERE key='banner_config'").fetchone()
        if not row:
            return dict(DEFAULT_BANNER)
        try:
            saved = json.loads(row['value'])
            return {**DEFAULT_BANNER, **{k: v for k, v in saved.items() if k in DEFAULT_BANNER and isinstance(v, str)}}
        except Exception:
            return dict(DEFAULT_BANNER)


@app.put('/api/admin/banner')
def update_banner(body: BannerConfig, request: Request):
    require(request, admin=True, write=True)
    payload = {k: v.strip() for k, v in _model_to_dict(body).items()}
    with database() as db:
        db.execute(
            "INSERT INTO site_settings(key, value) VALUES('banner_config', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (json.dumps(payload, ensure_ascii=False),),
        )
    return {'ok': True, 'banner': payload}


@app.get('/api/site-config')
def public_site_config():
    with database() as db:
        cfg = load_site_config(db)
    active_promos = [pr for pr in cfg['promos'] if pr['active']] if cfg['enable_promos'] else []
    public_promos = [
        {
            'code': pr['code'],
            'type': pr['type'],
            'value': pr['value'],
            'min_order': pr['min_order'],
            'max_discount': pr['max_discount'],
            'label': pr['label'],
        }
        for pr in active_promos
        if pr['show_public']
    ]
    return {
        'store_name': cfg['store_name'],
        'store_tagline': cfg['store_tagline'],
        'contact_name': cfg['contact_name'],
        'contact_phone': cfg['contact_phone'],
        'contact_note': cfg['contact_note'],
        'theme_preset': cfg['theme_preset'],
        'show_advisor': cfg['show_advisor'],
        'show_coming_soon': cfg['show_coming_soon'],
        'enable_promos': cfg['enable_promos'] and len(active_promos) > 0,
        'enable_shipping_fee': cfg['enable_shipping_fee'],
        'freeship_threshold': cfg['freeship_threshold'],
        'shipping_fee': cfg['shipping_fee'],
        'categories': cfg['categories'],
        'public_promos': public_promos,
    }


@app.get('/api/admin/site-config')
def admin_get_site_config(request: Request):
    require(request, admin=True)
    with database() as db:
        return load_site_config(db)


@app.put('/api/admin/site-config')
def admin_update_site_config(body: dict, request: Request):
    require(request, admin=True, write=True)
    with database() as db:
        db.execute(
            "INSERT INTO site_settings(key, value) VALUES('site_config', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (json.dumps(body, ensure_ascii=False),),
        )
        cfg = load_site_config(db)
    return {'ok': True, 'config': cfg}


@app.post('/api/promo/validate')
def validate_promo(body: dict):
    code = str((body or {}).get('code', '')).strip().upper()
    subtotal = max(0, int((body or {}).get('subtotal', 0) or 0))
    if not code:
        return {'valid': False, 'discount': 0, 'error': 'Vui lòng nhập mã giảm giá'}
    with database() as db:
        cfg = load_site_config(db)
    if not cfg.get('enable_promos'):
        return {'valid': False, 'discount': 0, 'error': 'Hiện chưa có chương trình mã giảm giá'}
    matched = next((pr for pr in cfg['promos'] if pr['code'] == code and pr['active']), None)
    if not matched:
        return {'valid': False, 'discount': 0, 'error': 'Mã giảm giá không hợp lệ hoặc đã hết hạn'}
    if subtotal < matched['min_order']:
        min_fmt = f"{matched['min_order']:,}".replace(',', '.') + 'đ'
        return {'valid': False, 'discount': 0, 'error': f'Mã {code} áp dụng cho đơn từ {min_fmt}'}
    if matched['type'] == 'percent':
        discount = round(subtotal * matched['value'] / 100)
        if matched['max_discount'] > 0:
            discount = min(discount, matched['max_discount'])
    else:
        discount = matched['value']
    discount = min(subtotal, max(0, discount))
    return {'valid': True, 'code': code, 'discount': discount}


app.mount('/', StaticFiles(directory=WEB, html=True), name='web')
