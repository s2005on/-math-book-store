# Trạng thái đồng bộ GitHub ↔ bản chạy Windows

**Ngày đối chiếu: 17/11/2026**. Đây là tình trạng được kiểm tra từ repo; không thay cho biên bản nghiệm thu của giảng viên.

| Mục | GitHub `main` trước PR quy trình | ZIP local người dùng đã nhận |
|---|---|---|
| Phiên bản | `VERSION=0.5.1` | `v0.6.0` |
| Tài khoản, quản trị sách | Có | Có |
| Banner sách sắp ra mắt | Có | Có |
| Đơn hàng lưu trong SQLite | **Chưa có trong phiên bản GitHub hiện tại** | Có trong ZIP local |
| Quản lý trạng thái đơn | **Chưa có trong phiên bản GitHub hiện tại** | Có trong ZIP local |
| Ảnh catalog | Thumbnail nhỏ, khoảng 131–240 px cạnh ngang | Có bộ ảnh WebP chất lượng cao |
| Pipeline ZIP | Trước PR bị sai tên file khi upload | ZIP local đã được tạo riêng |

## Việc cần làm trước khi tạo release v0.6.0 trên GitHub

1. Đối chiếu nguồn từ `LTDs-Book-Store-v0.6.0-Hoan-Chinh.zip` với `main` của GitHub (đặc biệt `server/app.py`, `server/web/*`, `tests/*`).
2. Nhập **cả mã nguồn và ảnh sách độ phân giải cao**, không chỉ đổi số phiên bản. Giữ bìa nguyên bản.
3. Xác minh giá: HSG Toán 8 **198.000đ**; Toán tổ hợp và tư duy logic **280.000đ**, trạng thái **sắp ra mắt**; xác nhận các giá khác với dữ liệu người bán.
4. Chạy test Python/Node, thêm test cho tạo đơn, lịch sử, quyền truy cập, giá/tồn kho. Chụp minh chứng desktop và mobile.
5. Xem lại [PR #2](https://github.com/s2005on/LTDs-Book-Store/pull/2) từ bản cải thiện ảnh 0.4.1; không merge nguyên PR cũ nếu sẽ ghi đè mã mới.
6. Chỉ sau khi PR đồng bộ mã nguồn được merge và CI đạt mới cập nhật VERSION, CHANGELOG và công bố tag/release **v0.6.0**.

## Các điều không nên làm

- Không copy `server/data/` từ máy sử dụng thực tế vào GitHub.
- Không đẩy `.env`, mật khẩu, số điện thoại hoặc địa chỉ khách hàng lên Git.
- Không tuyên bố phiên bản mới đã chạy trên VPS; hiện ưu tiên bản chạy Windows local.
- Không gắn tag mới lên mã GitHub cũ rồi gọi đó là bản 0.6.0.

**Nguồn:** cây file, VERSION và CI của LTD's Book Store; bản ZIP v0.9.0 được cung cấp trong cuộc trò chuyện.
