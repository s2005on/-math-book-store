# Trạng thái đồng bộ repository và gói Windows

**Đối chiếu: 17/11/2026**

| Thành phần | GitHub `main` hiện tại | ZIP LTD v0.9.0 |
|---|---|---|
| Repository | [s2005on/LTDs-Book-Store](https://github.com/s2005on/LTDs-Book-Store), đã đổi tên | `LTDs-Book-Store` |
| Phiên bản mã nguồn | `VERSION=0.5.1` | `VERSION=0.9.0` |
| Nhận diện thương hiệu | Đã có LTD's | Đã có LTD's |
| Đăng nhập và quản trị sách | Có | Có |
| Banner sắp ra mắt | Có | Có |
| Đặt hàng/hủy đơn/lịch sử | Chưa đầy đủ như ZIP | Có, lưu SQLite |
| Quản trị đơn hàng | Chưa có như ZIP | Có |
| Ảnh bìa | Thumbnail có ảnh chỉ vài KB | WebP chất lượng cao và ảnh gốc |
| Giá HSG Toán 8 | Cần kiểm tra sau nhập | 198.000đ |
| Sách Toán tổ hợp và tư duy logic | Chưa đầy đủ | 280.000đ, sắp ra mắt |
| Kiểm thử | CI hiện tại kiểm thử bản cũ | 16 Python + 4 JavaScript test đạt tại máy làm việc |

**Lưu ý:** bản ZIP v0.9.0 đã được kiểm thử riêng, không có nghĩa là CI của phiên bản v0.9.0 trên GitHub đã đạt. Chưa có Release chính thức cho v0.9.0.

## Tiêu chí cho PR nhập v0.9.0

- [x] Đổi tên repository mà không xóa lịch sử.
- [x] Chuẩn hóa ZIP nguồn, kiểm thử nội bộ 16 Python + 4 JavaScript.
- [ ] Push toàn bộ mã nguồn `server/`, `tests/`, `start.py`, `VERSION`, README.
- [ ] Push ảnh WebP chất lượng cao và thư mục `anh-goc/`.
- [ ] Không đẩy `.env`, `server/data/`, `.venv`, SQLite có thông tin khách hàng.
- [ ] Kiểm thử chức năng và giao diện desktop/mobile theo checklist.
- [ ] CI Ubuntu/Windows trên chính PR nhập v0.9.0 đạt.
- [ ] Merge PR, xác minh `main`, sau đó mới tag/release `v0.9.0`.

Hướng dẫn: [LTD-RENAME-AND-SYNC.md](LTD-RENAME-AND-SYNC.md) · [Issue #3](https://github.com/s2005on/LTDs-Book-Store/issues/3).
