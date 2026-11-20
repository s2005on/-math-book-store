# Changelog — LTD's Book Store

## v1.3.0 Pro Edition

Đồng bộ ứng dụng, kiểm thử và ảnh từ bản Pro. Bổ sung hồ sơ Buổi 9, kế hoạch cá nhân và ca nghiệm thu luồng đơn hàng. [Chi tiết phiên bản](RELEASE-NOTES-v1.3.0.md).

## v0.5.1 — Sửa khởi chạy Windows

- Chạy lại `start.py` trong môi trường `.venv` sau khi cài thư viện để khắc phục lỗi thiếu `dotenv`.
- Thêm đăng nhập/đăng ký, quản trị sách, upload ảnh, SQLite và trạng thái còn hàng/hết hàng/sắp ra mắt từ các lượt nâng cấp v0.4–v0.5.
- Hệ thống checkout trên nhánh hiện tại vẫn là **demo**, chưa nhận đơn hàng thực.

## Quy trình phát hành (đang triển khai)

- Sửa CI tự đóng gói ZIP theo `VERSION`, tránh sai tên v0.5.0/v0.5.1.
- Thêm xác minh tính toàn vẹn ZIP và bước phát hành sau tag.
- **Bản ZIP local v0.6.0 chưa đồng bộ mã nguồn lên GitHub**; không tuyên bố mã hiện tại đã có module đơn hàng của bản ZIP.

## v0.3.0 — Book mockup storefront

- Hoàn thiện nhận diện cửa hàng sách theo tông xanh navy – kem – đồng.
- Làm nổi bật ảnh sản phẩm dạng cuốn sách, không chỉnh sửa thiết kế bìa gốc.
- Hoàn thiện bộ lọc lớp, tìm kiếm, sắp xếp, chi tiết sách và giỏ hàng.
- Bổ sung ghi chú rõ ràng rằng checkout hiện là demo, chưa tiếp nhận đơn thật.
- Chuẩn bị workflow xuất bản giao diện tĩnh lên GitHub Pages.
- Chạy lại 9 bài kiểm thử tự động: 5 Python smoke tests và 4 Node catalog tests.


## v0.2.0 — UI Foundation
- Storefront sách Toán, danh mục, tìm kiếm, lọc, sắp xếp.
- Giỏ hàng demo, chi tiết sản phẩm, checkout minh họa.
- Header và thanh giỏ hàng cố định, responsive.
- Admin UI preview, FastAPI static host, health endpoint.
- Ảnh bìa mockup từ ảnh sách do người dùng cung cấp.
- Tài liệu đồ án, test plan, CI Ubuntu/Windows và hướng dẫn deploy.
- Backend nhận đơn, database, đăng nhập và thanh toán chưa triển khai.

## v0.1.0 — Initial Demo
- Khung giao diện cửa hàng và dữ liệu sản phẩm mẫu.
