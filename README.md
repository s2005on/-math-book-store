# Math Book Store — Website bán sách Toán

![CI](https://github.com/s2005on/-math-book-store/actions/workflows/ci.yml/badge.svg?branch=main)

Website bán sách tham khảo Toán lớp 6–9 và tài liệu ôn thi vào lớp 10. Dự án độc lập, tham khảo quy trình tổ chức repository, tài liệu, kiểm thử và release của [VNU Food Hola](https://github.com/s2005on/vnu-food-hola), không sao chép mã nguồn.

> **Trạng thái: v0.2.0 — UI Foundation.** Bản hiện tại là storefront và giỏ hàng demo; chưa có API đơn hàng, database, đăng nhập quản trị hoặc thanh toán. Không sử dụng để nhận đơn thật.

## Chạy nhanh
Yêu cầu Python 3.11+.

**Windows:** chạy `RUN-WINDOWS.bat`, sau đó mở http://127.0.0.1:8017/

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r server/requirements.txt
python -m uvicorn server.app:app --host 127.0.0.1 --port 8017
```
Không mở HTML trực tiếp bằng `file://`; cần server để tải catalog.

## Chức năng UI Foundation
- Danh mục sách theo lớp, tìm kiếm, lọc và sắp xếp.
- Chi tiết sách, giỏ hàng lưu trên trình duyệt, tính tổng.
- Checkout minh họa, không gửi/lưu đơn hàng.
- Header và thanh giỏ hàng cố định, responsive.
- Admin UI preview, health endpoint.
- Ảnh bìa mockup được xử lý từ ảnh sách do người dùng cung cấp.

## Kiểm thử
```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -v
node --test tests/*.test.cjs
```

## Cấu trúc
```text
.github/       CI, issue/PR templates
deploy/        Nginx, systemd, hướng dẫn VPS
docs/          Charter, requirements, design, WBS, tests, sprint, release
server/        FastAPI static host và storefront
  web/         HTML, CSS, JS, catalog JSON, ảnh bìa
tests/         Python smoke tests và Node catalog tests
```

## Dữ liệu sách mẫu
| Sản phẩm | Giá tham khảo |
|---|---:|
| Bài tập thực hành Toán 6–9, mỗi bộ 2 tập | 80.000đ/bộ |
| Luyện thi vào lớp 10 – Đại số & Hình học | 270.000đ/bộ |
| Chinh phục đề thi học sinh giỏi Toán 8 | 198.000đ |
| 63 đề ôn thi vào lớp 10 môn Toán | Chưa xác nhận |

Giá là dữ liệu mẫu từ trao đổi ban đầu, cần xác nhận trước khi kinh doanh.

## Lộ trình
1. Sprint 0: UI Foundation.
2. Sprint 1: Catalog/Admin API, database, xác thực.
3. Sprint 2: Đơn hàng, trạng thái, thông báo.
4. Sprint 3: hardening, bảo mật, backup, nghiệm thu và VPS.

Xem [docs/README.md](docs/README.md).