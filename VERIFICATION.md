# Verification — Math Book Store

## Đối chiếu ngày 17/11/2026

Mã trên GitHub `main` là v0.5.1 (chưa nhập mã nguồn ZIP v0.6.0). Không dùng kết quả kiểm thử một bản để xác nhận bản còn lại.

- GitHub Actions trên commit `f3e7aa8` báo **failure**, nhưng log cho thấy Python unittest, JS syntax và Node catalog tests **đã đạt** ở cả Ubuntu/Windows.
- Lỗi CI thực tế: `scripts/package.py` tạo `Math-Book-Store-v0.5.1.zip` nhưng workflow cũ tìm `Math-Book-Store-v0.5.0.zip`.
- PR `fix/ci-release-workflow` khắc phục bằng cách dùng VERSION và wildcard, xác minh ZIP; kết quả sau merge xem GitHub Actions.
- Bản ZIP local v0.6.0 đã được kiểm thử ở lượt làm trước, nhưng chưa đối chiếu bằng test ở trên repo GitHub.

## Những phần cần kiểm tra thêm

- Đồng bộ đầy đủ backend đơn hàng và ảnh nét cao từ ZIP v0.6.0 vào PR khác.
- Kiểm thử thủ công ở desktop/mobile, đặc biệt ảnh và trạng thái sách, cache trình duyệt.
- Backup/restore và dữ liệu thật; chưa triển khai VPS.
- Không cam kết có payment gateway hay bảo mật production chỉ từ các bài test local.

[CI trên GitHub](https://github.com/s2005on/-math-book-store/actions) · [Quy trình](docs/WORKFLOW.md) · [Chênh lệch repo/ZIP](docs/REPO-SYNC-STATUS.md)
