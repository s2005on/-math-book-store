# Đổi tên repository và đồng bộ LTD's Book Store

**Tên hiển thị:** LTD's Book Store  
**Tên repository mục tiêu:** `s2005on/LTDs-Book-Store`  
**ZIP người dùng cung cấp:** `LTDs-Book-Store-v0.9.0.zip` (tên bên trong còn `Math-Book-Store`, VERSION cũ `0.6.0`).

## 1. Đổi tên repository mà không mất lịch sử

Kết nối GitHub hiện có hỗ trợ đọc/ghi mã nguồn, tạo nhánh/PR/merge, **không hỗ trợ thao tác Settings đổi repository name**. Chủ tài khoản cần mở:

[Repository Settings](https://github.com/s2005on/-math-book-store/settings) → **General** → **Repository name** → nhập `LTDs-Book-Store` → **Rename**.

GitHub thường tự chuyển hướng URL repository cũ sang URL mới. Dù vậy hãy cập nhật remote của bản clone cục bộ:

```bash
git remote set-url origin https://github.com/s2005on/LTDs-Book-Store.git
git remote -v
```

Nếu tên bị trùng/không hợp lệ, GitHub sẽ báo tại giao diện. Không tạo repository mới rồi xóa repository cũ: sẽ mất liên kết lịch sử PR/issue.

## 2. Điều đã đồng bộ trong PR nhận diện

- Tên **LTD's Book Store** trên trang chủ, login, tài khoản, admin, FastAPI và tài liệu.
- Tên ZIP trong script `LTDs-Book-Store-v<VERSION>.zip`; CI và release workflow tương ứng.
- Slug `ltds-book-store` ở các chỗ dùng làm định danh dự án.
- Biến môi trường chính thức `LTDS_*` cho backend; hỗ trợ đọc các biến `MBS_*` cũ để tránh phá đường dẫn dữ liệu.
- Giỏ hàng dùng khóa localStorage LTD mới; khi chưa có dữ liệu mới sẽ đọc khóa cũ để giữ giỏ hàng.

## 3. Phân biệt **đổi thương hiệu** với **đồng bộ phiên bản**

GitHub `main` vẫn chứa mã v0.5.1 và thumbnail cũ. File ZIP của người dùng chứa v0.9.0 với các tính năng/ảnh mới. Đổi tên hiển thị không biến mã v0.5.1 thành v0.9.0.

Để thực sự nhập bản v0.9.0 vào repo:
1. Giữ nguyên lịch sử Git và cấu trúc `.github/`, `docs/` đã có.
2. Tạo nhánh `feat/import-ltd-v0.9.0` từ `main`.
3. Chép các tệp ứng dụng, thử nghiệm, ảnh WebP độ phân giải cao và thư mục `anh-goc` từ ZIP đã chuẩn hóa vào nhánh, **không chép `server/data/`, `.env`, `.venv`, `__pycache__`**.
4. Chạy Python unittest và Node tests; kiểm thử đăng nhập, thêm sách, giỏ hàng, đặt đơn, quản trị đơn, banner.
5. Cập nhật `VERSION` thành `0.9.0` **khi source đã đầy đủ**; giữ tên branding LTD, kiểm tra chính xác tên ZIP và CI.
6. Mở Pull Request, đợi CI cả Windows/Ubuntu đạt, merge rồi mới công bố tag/release `v0.9.0`.

Xem [Issue đồng bộ mã](https://github.com/s2005on/-math-book-store/issues/3). Chưa có VPS, không công bố địa chỉ web public hoặc tuyên bố đã xử lý giao dịch thật.

## 4. Dữ liệu và thanh toán

Giữ các đầu sách, giá và trạng thái từ ZIP nguồn. Bản đồ án có nội dung VietQR/MoMo/VNPAY **mô phỏng**, không xác nhận thanh toán thật; không commit tài khoản ngân hàng, mật khẩu, khách hàng hoặc bản sao SQLite lên repo công khai.
