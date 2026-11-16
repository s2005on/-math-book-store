# Bàn giao Sprint 0 — UI Foundation

## Đã đồng bộ lên GitHub main

- Storefront responsive và admin UI preview.
- Catalog 7 đầu sách mẫu, trong đó một đầu sách chưa có giá xác nhận.
- 7 ảnh mockup sản phẩm đã xử lý; ảnh nguồn riêng không được đưa vào repository công khai.
- FastAPI static host và endpoint `/health`.
- Giỏ hàng demo, tìm kiếm, lọc, sắp xếp và chi tiết sản phẩm.
- Python smoke tests, Node catalog tests, GitHub Actions workflow.
- Project charter, requirements, system design, WBS, schedule, Scrum, backlog, demo script, test plan, release checklist và tài liệu quản trị dự án.

## Kiểm tra

- Python: 5/5 tests đạt.
- Node.js: 4/4 tests đạt.
- GitHub Actions trên Ubuntu / Python 3.12: đạt.
- GitHub Actions trên Windows / Python 3.12: đạt.
- Pull Request #1 đã merge vào `main`.
- Merge commit: `d987f5e69d9726cc358926f6f8c610e3569c04ad`.

## Chưa triển khai

- API nghiệp vụ, database và CRUD sản phẩm.
- Đăng nhập quản trị và phân quyền.
- Nhận/lưu đơn hàng thật, trạng thái đơn và thanh toán.
- Tồn kho, thông báo, vận chuyển và chính sách đổi/trả.
- Domain, HTTPS, backup và cấu hình production.

## Trạng thái release và VPS

Mã nguồn UI Foundation đã nằm trên nhánh `main`. Chưa tạo Git tag/GitHub Release chính thức. Chưa triển khai lên VPS; VPS do chủ dự án tự quản lý.

## Việc tiếp theo

1. Xác nhận tên sách, giá và quyền sử dụng ảnh với người bán.
2. Chốt yêu cầu học phần và phạm vi Sprint 1.
3. Xây dựng Catalog API, database và quản trị có xác thực.
4. Xây dựng đơn hàng, kiểm thử bảo mật và chuẩn bị triển khai production.
5. Sau khi hoàn tất kiểm tra phát hành, tạo tag và GitHub Release cho phiên bản tương ứng.
