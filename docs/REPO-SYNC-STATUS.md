# Trạng thái đồng bộ repository và gói Windows

**Đối chiếu cập nhật: 17/11/2026**. Phiên bản GitHub `main` vẫn là **0.5.1**, chưa chứa đầy đủ ZIP local **LTD's Book Store v1.2.0 Art Edition**.

| Thành phần | GitHub `main` hiện tại | Art Edition v1.2.0 đã chuẩn hóa local |
|---|---|---|
| Repository | [s2005on/LTDs-Book-Store](https://github.com/s2005on/LTDs-Book-Store) | Cùng dự án |
| VERSION | `0.5.1` | `1.2.0` |
| Nhận diện | LTD's Book Store | LTD's Book Store |
| Đăng nhập, quản trị sách | Có mã | Có mã |
| Đơn hàng, lịch sử/hủy đơn | Chưa có đầy đủ | Có, lưu trong SQLite |
| Moderator/banner/khuyến mãi | Chưa đầy đủ | Có giao diện và backend |
| Ảnh sách | Thumbnail cũ | 11 WebP chất lượng cao + 10 ảnh gốc |
| Chế độ sáng/tối | Chưa có | Có |
| Giá HSG Toán 8 | 198.000đ (catalog hiện tại cần xác nhận lại) | 198.000đ |
| Toán tổ hợp và tư duy logic | Dữ liệu cũ | 280.000đ, sắp ra mắt |
| Test | CI Windows/Ubuntu cho mã v0.5.1 | 17 Python + 4 Node đạt trên bản local chuẩn hóa |
| GitHub CI v1.2 | **Chưa chạy** | Chưa nhập vào PR |

## Vấn đề đã phát hiện trong ZIP đầu vào

ZIP được đặt tên v1.2.0 nhưng `VERSION` và README bên trong còn ghi v0.6.0, thư mục gốc còn tên Math Book Store. Đã chuẩn hóa các nội dung này trong **bản ZIP local sửa lỗi**, chưa đồng bộ toàn bộ ảnh nhị phân và mã lên GitHub.

## Tiêu chí nhập phiên bản v1.2.0

- [x] Kiểm tra nội dung ZIP và xác nhận ảnh/giá/đơn hàng trên bản local.
- [x] Chuẩn hóa nhận diện, VERSION, smoke tests và lỗi tràn tablet trong gói local.
- [ ] Push toàn bộ `server/`, `tests/`, `start.py`, ảnh WebP và `anh-goc/` vào nhánh riêng.
- [ ] Không đẩy `.env`, `server/data/`, `.venv`, SQLite hoặc dữ liệu khách.
- [ ] CI Windows/Ubuntu và test giao diện trên **đúng commit** đạt.
- [ ] Merge PR, xác minh `main`, sau đó mới tạo tag/Release `v1.2.0`.

[Biên bản tiếp nhận](RELEASE-INTAKE-v1.2.0.md) · [Issue #10](https://github.com/s2005on/LTDs-Book-Store/issues/10). Bản v0.9.0 trước đây chỉ là mốc local cũ, **không phải release đã đồng bộ trên GitHub**.
