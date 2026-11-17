# Tiếp nhận bản LTD's Book Store v1.2.0 — Art Edition

**Ngày tiếp nhận:** 17/11/2026. **Tình trạng:** đang chờ PR đồng bộ mã nguồn và ảnh; **không phải GitHub Release đã được phát hành**.

## 1. Tệp chủ dự án cung cấp

- Tên ZIP: `LTDs-Book-Store-v1.2.0-Art-Edition.zip`.
- Nội dung: 56 tệp, khoảng 19,8 MB nén; 11 ảnh WebP hiển thị và 10 ảnh nguồn JPG/PNG.
- **Sai lệch phát hiện:** tệp `VERSION` bên trong vẫn ghi `0.6.0`, thư mục ZIP và tài liệu chạy local vẫn ghi tên Math Book Store. Không đẩy nguyên ZIP lên main mà chưa chuẩn hóa.
- Sau chuẩn hóa local: `VERSION=1.2.0`, nhận diện LTD, giữ nguyên bìa sách, sửa tràn thanh tác vụ tablet và bổ sung test.

## 2. Tính năng và kiểm thử trên bản đã chuẩn hóa

- Khách hàng: danh mục, tìm kiếm/lọc, yêu thích, giỏ, đăng nhập, đặt đơn thử nghiệm trong SQLite, xem/hủy đơn.
- Quản trị Moderator: CRUD sản phẩm, tải ảnh, trạng thái, quản lý đơn, banner, cấu hình giao diện và mã giảm giá.
- Art Edition: giao diện sáng/tối, card sách 3D, nút về đầu trang.
- **Đây là thanh toán demo**: COD/VietQR/MoMo/VNPAY chưa kết nối cổng, không thu tiền, QR chỉ minh họa.
- 17/17 Python test trên mã ZIP local đã chuẩn hóa; 4/4 Node test + JS syntax.
- Kiểm thử Chromium **với API mô phỏng** trên 1440/768/390/360px; không còn tràn ngang, 7 sản phẩm bán và 2 sách sắp ra mắt. Không được coi là bằng chứng chạy E2E với máy chủ thực hoặc GitHub CI.
- Giá HSG Toán 8 **198.000đ** và Toán tổ hợp – tư duy logic **280.000đ**, sắp ra mắt, khóa mua.

## 3. So với mã GitHub

| Hạng mục | `main` hiện tại | Bản Art Edition local |
|---|---|---|
| VERSION | 0.5.1 | 1.2.0 sau chuẩn hóa |
| Đặt hàng, khuyến mãi, Moderator | Chưa đầy đủ | Có mã và test riêng |
| Bìa sách nét cao và `anh-goc/` | Chưa đầy đủ | Có |
| GitHub CI Windows/Ubuntu trên phiên bản 1.2 | **Chưa chạy** | Chưa nhập vào PR |

## 4. Yêu cầu để hoàn thành đồng bộ

- Theo dõi [Issue #10](https://github.com/s2005on/LTDs-Book-Store/issues/10).
- Import **toàn bộ ảnh nhị phân** và mã/test bằng nhánh riêng; giữ nguyên hệ thống docs/CI hiện có.
- Bảo đảm không commit `.env`, SQLite khách hàng, `server/data/`, `.venv/`.
- Review nội dung + CI Ubuntu/Windows xanh trên commit nhập mã.
- Chỉ sau khi merge mới đổi `VERSION` của main theo đúng code, tạo tag và GitHub Release v1.2.0.

**VPS đang tạm hoãn**, không đồng bộ dữ liệu người dùng thực lên GitHub.
