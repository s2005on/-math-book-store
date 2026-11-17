# 03 — Thiết kế hệ thống LTD's Book Store

## 1. Phiên bản và phạm vi được mô tả

Tài liệu này mô tả **mã nguồn thực có trên GitHub `main` v0.5.1** tại thời điểm xây dựng hồ sơ, **không phải toàn bộ chức năng trong ZIP local v1.2.1**. Bản v1.2.1 cần [nhập và kiểm thử riêng](REPO-SYNC-STATUS.md) trước khi cập nhật sơ đồ. Không có VPS production trong phạm vi này.

## 2. Kiến trúc thực tế

```text
Trình duyệt người mua / quản trị
  |  HTML/CSS/JavaScript: server/web/
  |  Giỏ hàng localStorage (không phải đơn đã gửi)
  |  Cookie đăng nhập HttpOnly + CSRF khi ghi dữ liệu
  v
FastAPI — server/app.py (127.0.0.1:8017)
  |- /health
  |- /api/books (đọc công khai)
  |- /api/register, /api/login, /api/logout, /api/me
  |- /api/admin/books + /api/admin/books/{id} (CRUD quản trị)
  |- /api/admin/upload, /api/images/{name}
  |- StaticFiles: giao diện và ảnh bìa
  v
SQLite: server/data/shop.sqlite3 (users, sessions, books, seed_history)
Filesystem: server/data/uploads/ (ảnh upload)
```

**Điều đã triển khai:** đăng ký, đăng nhập, phân quyền admin, danh mục sách, CRUD, ảnh upload, trạng thái bán, cửa hàng và giỏ hàng mẫu. **Điều chưa có trong mã GitHub v0.5.1:** lưu đơn thật, lịch sử đơn và quản lý trạng thái đơn. Checkout tại phiên bản này là demo.

## 3. Các endpoint có trên `main`

| Phương thức | URL | Ý nghĩa |
|---|---|---|
| GET | `/health` | kiểm tra máy chủ |
| GET | `/api/books` | danh sách sản phẩm/trạng thái |
| GET | `/api/me` | trạng thái đăng nhập |
| POST | `/api/register` | tạo tài khoản khách |
| POST | `/api/login` | đăng nhập, cấp cookie phiên |
| POST | `/api/logout` | kết thúc phiên |
| POST | `/api/admin/books` | quản trị thêm sách |
| PUT | `/api/admin/books/{id}` | quản trị sửa sách |
| DELETE | `/api/admin/books/{id}` | quản trị xóa sách |
| POST | `/api/admin/upload` | quản trị tải ảnh (JPG/PNG/WebP) |
| GET | `/api/images/{name}` | trả ảnh đã tải |

Không liệt kê API đơn hàng của ZIP v1.2.1 ở đây cho đến khi PR nhập phiên bản được merge.

## 4. Mô hình dữ liệu và quy tắc

- `users`: tên đăng nhập, mật khẩu hash PBKDF2, quyền (`admin`/`customer`).
- `sessions`: lưu hash phiên, mã CSRF, thời hạn.
- `books`: ID, tên, danh mục, giá, ảnh, nhãn, mô tả, thứ tự hiển thị, tình trạng.
- `seed_history`: dấu mốc dữ liệu mẫu đã khởi tạo để tránh thêm lại khi quản trị xóa.

Trạng thái sản phẩm gồm `available`, `sold_out`, `coming_soon`. Sách sắp ra mắt và hết hàng không được thêm vào giỏ. Các thao tác ghi ở API admin kiểm tra phiên, vai trò và CSRF phía máy chủ.

## 5. Quyết định thiết kế, giới hạn và an toàn

- Chạy local; `server/data/` không được commit, cần sao lưu trước khi nâng cấp.
- `.env` chứa cấu hình admin; không cho lên GitHub. Khi mở mạng công cộng cần HTTPS, Secure cookie, audit bảo mật trước khi sử dụng thực.
- Ảnh bìa gốc giữ nguyên thiết kế, chỉ tối ưu hiển thị; ảnh chất lượng cao của ZIP v1.2.1 chưa đồng bộ vào `main`.
- `catalog.json` hỗ trợ fallback frontend nhưng nguồn dữ liệu động khi server hoạt động là API SQLite.
- Tài khoản khách có thể đăng nhập; chưa có thanh toán tự động, email, phục hồi mật khẩu hoặc vận chuyển thật.

## 6. Kiến trúc mục tiêu (chưa tính là đã làm)

Sau khi nhập ZIP v1.2.1, bổ sung sơ đồ bảng `orders` và các API tạo đơn, lịch sử, hủy, quản trị trạng thái dựa trên **mã thực tế đã kiểm thử**, đồng thời cập nhật [TEST-PLAN.md](TEST-PLAN.md) và bằng chứng cho đúng commit.
