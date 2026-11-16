# 01 — Project Charter

## Thông tin dự án

- **Tên đề tài:** Xây dựng website thương mại điện tử bán sách tham khảo Toán.
- **Tên dự án:** LTD's Book Store.
- **Loại sản phẩm:** Website responsive, mô hình cửa hàng đơn lẻ.
- **Trạng thái gốc của tài liệu:** UI Foundation — Sprint 0 (lịch sử giai đoạn khởi tạo).
- **Nguồn tham khảo quy trình:** VNU Food Hola (`s2005on/vnu-food-hola`).

## Bối cảnh và vấn đề

Người học cần tìm sách theo khối lớp và mục tiêu học tập; thông tin bìa, bộ sách và giá cần được trình bày rõ ràng. Người bán cần một nơi giới thiệu danh mục, cập nhật sản phẩm và tiếp nhận đơn hàng có cấu trúc.

## Mục tiêu

1. Xây dựng giao diện cửa hàng dễ sử dụng trên máy tính và điện thoại.
2. Hỗ trợ duyệt sách theo lớp, tìm kiếm, xem chi tiết và quản lý giỏ hàng.
3. Chuẩn bị kiến trúc repository, tài liệu, kiểm thử và quy trình release để mở rộng thành ứng dụng có backend.
4. Xây dựng giao diện quản trị minh họa cho giai đoạn tiếp theo.

## Các bên liên quan

- Người mua: tìm kiếm, chọn sách và đặt hàng.
- Người bán/quản trị: cung cấp ảnh, thông tin, giá và xử lý đơn.
- Người thực hiện đồ án: phân tích, thiết kế, lập trình, kiểm thử và bàn giao.
- Giảng viên: hướng dẫn và đánh giá kết quả học phần.

## Phạm vi Sprint 0

Bao gồm storefront, responsive UI, catalog JSON mẫu, cart demo, mockup ảnh bìa, admin UI preview, FastAPI static host, health check, tài liệu và CI.

Không bao gồm API đơn hàng thật, database, tài khoản, thanh toán, tồn kho, vận chuyển hoặc gửi thông báo.

## Tiêu chí hoàn thành Sprint 0

- Trang cửa hàng tải được danh mục từ JSON.
- Tìm kiếm, lọc, sắp xếp và giỏ hàng hoạt động trên trình duyệt.
- Biểu mẫu demo không gửi/lưu thông tin cá nhân.
- Ảnh bìa sản phẩm được xử lý từ nguồn ảnh người bán cung cấp.
- Có thể chạy local bằng hướng dẫn trong README.
- Kiểm thử tự động và CI chạy qua.

## Cập nhật tình trạng mã nguồn GitHub

Từ sau Sprint 0, `main` v0.5.1 đã có FastAPI, SQLite, đăng ký/đăng nhập và CRUD sách; vì vậy phần **Phạm vi Sprint 0** ở trên chỉ mô tả phạm vi lúc bắt đầu, **không** mô tả toàn bộ phần mềm hiện tại. Chức năng đơn hàng và ảnh độ phân giải cao của ZIP v0.9.0 chưa đồng bộ lên `main`. Theo dõi [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md) và [ACADEMIC-TRACEABILITY.md](ACADEMIC-TRACEABILITY.md).
