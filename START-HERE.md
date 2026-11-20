# Chạy LTD's Book Store v1.3.0 Pro Edition trên Windows

1. Cài Python 3.11 trở lên và chọn **Add python.exe to PATH** trong bộ cài.
2. Tải mã nguồn của commit cần chạy, giải nén vào một thư mục riêng.
3. Mở thư mục chứa `VERSION` và nhấp đúp `RUN-WINDOWS.bat`. Lần đầu cần Internet để cài phụ thuộc. Làm theo lời nhắc tạo tài khoản quản trị.
4. Mở http://127.0.0.1:8017/ để tìm sách. Dùng dữ liệu thử khi đăng ký và đặt đơn. Trang tài khoản ở `/account.html`, trang quản trị ở `/admin.html`.
5. Giữ cửa sổ lệnh mở khi dùng. Nhấn Ctrl+C để dừng. Khi dùng thư mục dữ liệu mặc định, chạy `BACKUP-WINDOWS.bat` sau khi dừng để sao lưu `server/data/`.

Nếu cửa sổ đóng sớm, mở CMD trong thư mục vừa giải nén rồi chạy `RUN-WINDOWS.bat` để đọc thông báo lỗi. Nếu cổng 8017 đang được dùng bởi một bản LTD khác, dừng bản đó trước khi chạy lại.

[Hồ sơ Buổi 9](docs/B9.md) · [Chức năng bản Pro](RELEASE-NOTES-v1.3.0.md)
