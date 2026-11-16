# Math Book Store v0.4.1 — đồ án bán sách

Repo riêng tham khảo luồng trải nghiệm từ [VNU Food Hola](https://github.com/s2005on/vnu-food-hola). Giao diện trang chủ giữ màu xanh lá/kem/cam hiện có; KHÔNG thay đổi ảnh bìa sách gốc và KHÔNG thay đổi repo bán đồ ăn.

## Tính năng
- Cửa hàng: lọc/tìm kiếm sách, phân loại theo lớp, xem chi tiết, giỏ hàng và checkout **demo**.
- Tài khoản: đăng ký/đăng nhập khách hàng tại `/login.html`; quản trị viên có thể đăng nhập và đi đến `/admin.html`.
- Quản trị: thêm slot sách mới; tải ảnh JPG/PNG/WebP tối đa 5 MB; sửa tên, mô tả, giá, danh mục, tình trạng **còn hàng/hết hàng**, xóa sách.
- Ảnh upload được chuyển sang WebP và lưu phía máy chủ.
- Ảnh upload lưu WebP quality 96; bộ ảnh catalog mới giữ độ phân giải gốc và không chỉnh sửa nội dung bìa. Sản phẩm hết hàng bị khóa thêm giỏ hàng.
- Dữ liệu sách/tài khoản trong SQLite, ảnh trong `MBS_DATA_DIR/uploads`.
- **63 đề ôn thi vào lớp 10: 139.000đ** theo giá vừa nhận. Cuốn HSG lớp 7 chưa in: chưa mở bán.

## Chạy local (FastAPI, Python 3.11+)
```bash
python -m pip install -r server/requirements.txt
# Thiết lập 2 biến môi trường trên máy chạy, không commit mật khẩu vào GitHub:
export MBS_ADMIN_USER=adminmath
export MBS_ADMIN_PASSWORD='THAY_BANG_MAT_KHAU_MANH_TOI_THIEU_12_KY_TU'
export MBS_DATA_DIR=/opt/math-book-store-data
python -m uvicorn server.app:app --host 127.0.0.1 --port 8017
```
Trên Windows PowerShell dùng `$env:MBS_ADMIN_USER="adminmath"`, `$env:MBS_ADMIN_PASSWORD="..."` và `$env:MBS_DATA_DIR="..."`.

Mở `http://127.0.0.1:8017/`, `/login.html`, `/admin.html`, `/health`.
**Lưu ý:** tài khoản admin chỉ tự tạo khi lần đầu thiết lập và chưa tồn tại tên tương ứng. Thay đổi biến môi trường không đổi mật khẩu của admin đã tạo. Không dùng mật khẩu ví dụ trong thực tế.

## Chạy trên VPS / HTTPS
- Cấu hình domain và Nginx reverse proxy đến `127.0.0.1:8017`, bật HTTPS và set `MBS_SECURE_COOKIES=1`.
- Gắn volume bền vững cho `MBS_DATA_DIR`; sao lưu file SQLite **và** thư mục `uploads`.
- Giới hạn quyền hệ thống cho thư mục dữ liệu; không đặt thư mục SQLite bên trong `server/web`.
- Giữ bí mật mật khẩu admin ở VPS hoặc secrets; không đưa vào GitHub. Cần giám sát, backup, giới hạn đăng ký và kiểm thử trước khi mở cho người dùng thật.

## Chú ý GitHub Pages
GitHub Pages chỉ host file tĩnh. Trang chủ có thể hiển thị catalog từ `catalog.json`, nhưng **đăng nhập, upload ảnh, quản lý tồn kho và đồng bộ dữ liệu không hoạt động** trên Pages. Để dùng chức năng mới phải chạy FastAPI trên VPS. Nếu API không có, trang quản trị sẽ báo rõ.

## Kiểm thử
```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -v
node --check server/web/app.js
node --test tests/*.test.cjs
```

## Giới hạn
Checkout vẫn chỉ là mô phỏng, không gửi đơn thật, không có thanh toán thật. Chưa kiểm thử hệ thống trên VPS sản xuất. Không dùng thông tin cá nhân thật trong form checkout demo.
