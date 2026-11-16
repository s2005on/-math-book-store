# LTD's Book Store — bản chạy máy cá nhân v0.5.1

Website cửa hàng sách Toán với đăng nhập, quản lý kho sách và banner sách sắp ra mắt. Không cần VPS hay GitHub để chạy sau khi đã tải ZIP về máy.

## Cách chạy nhanh trên Windows

1. Cài **Python 3.11 trở lên** từ https://www.python.org/downloads/ (khi cài, chọn **Add Python to PATH**).
2. Giải nén toàn bộ file ZIP vào một thư mục, ví dụ `Desktop\\LTDs-Book-Store`.
3. Nhấn đúp **RUN-WINDOWS.bat**.
4. Lần đầu chạy, cửa sổ sẽ hỏi tên đăng nhập và mật khẩu quản trị (ít nhất 12 ký tự). Mật khẩu được lưu trong file `.env` trên máy.
5. Website tự mở tại http://127.0.0.1:8017/

Lần đầu cần Internet để tải thư viện Python. Những lần sau chạy lại `RUN-WINDOWS.bat`, không cần tạo tài khoản admin lần nữa.

## macOS / Linux

Cài Python 3.11+, mở Terminal tại thư mục đã giải nén và chạy:

```bash
chmod +x run.sh
./run.sh
```

## Các địa chỉ

- Trang cửa hàng: http://127.0.0.1:8017/
- Đăng nhập: http://127.0.0.1:8017/login.html
- Quản lý sách: http://127.0.0.1:8017/admin.html
- Kiểm tra hoạt động: http://127.0.0.1:8017/health

## Tính năng

- Đăng ký/đăng nhập khách hàng và tài khoản quản trị.
- Thêm sách mới, tải ảnh bìa JPG/PNG/WebP (tối đa 5 MB), sửa thông tin, giá, mô tả và xóa sách.
- Trạng thái: **Còn hàng**, **Hết hàng**, **Sắp ra mắt**.
- Sách sắp ra mắt tự hiển thị trong banner riêng; không thể thêm vào giỏ hàng.
- Tìm kiếm, lọc sách, xem chi tiết và giỏ hàng demo.

## Dữ liệu và an toàn

- Cơ sở dữ liệu SQLite và ảnh tải lên được lưu trong `server/data/`.
- File `.env` lưu thông tin khởi tạo admin. Không gửi file này cho người khác và không tải lên GitHub.
- Không xóa `server/data/` nếu muốn giữ tài khoản, sách và ảnh đã tải lên.
- Sao lưu định kỳ toàn bộ thư mục `server/data/`.
- Website mặc định chỉ truy cập trên máy đang chạy (`127.0.0.1`), không tự công khai lên Internet.

## Lưu ý

- Checkout hiện là bản demo, chưa gửi đơn hàng và chưa tích hợp thanh toán.
- Cần để cửa sổ terminal chạy nền trong lúc dùng website; nhấn Ctrl+C để dừng.
- Nếu cổng 8017 đang được ứng dụng khác sử dụng, hãy tắt ứng dụng đó rồi chạy lại.

## Bản sửa v0.5.1
- Bộ khởi chạy chuyển sang Python của `.venv` sau khi cài thư viện, xử lý lỗi `No module named 'dotenv'` trên Windows.
