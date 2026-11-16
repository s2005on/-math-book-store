# Lưu ý: Tài liệu lịch sử Sprint 0

Phần dưới lưu kịch bản giao diện ban đầu, **không** mô tả toàn bộ khả năng trên `main` v0.5.1. Chức năng đăng nhập và CRUD sách đã có, nhưng lưu đơn thật chưa có trên mã GitHub. Để demo bản hiện tại, xem [TEST-PLAN.md](TEST-PLAN.md), [SPRINT-TRACKER.md](SPRINT-TRACKER.md) và [ACADEMIC-TRACEABILITY.md](ACADEMIC-TRACEABILITY.md).

---

# 08 — Kịch bản demo trình bày đồ án

## Chuẩn bị

- Khởi chạy theo `START-HERE.md`.
- Mở website trên màn hình desktop và điện thoại.
- Chuẩn bị trình duyệt ở trạng thái giỏ hàng trống.

## Kịch bản khách hàng

1. Giới thiệu trang chủ và thông điệp của cửa hàng.
2. Cho thấy header bám trên đầu khi cuộn.
3. Chọn danh mục Lớp 8 để lọc hai sản phẩm.
4. Tìm kiếm `toan 9` để minh họa tìm kiếm không dấu.
5. Mở chi tiết sách Chinh phục đề thi học sinh giỏi Toán 8.
6. Thêm sách vào giỏ, tăng rồi giảm số lượng.
7. Cho thấy thanh giỏ hàng cố định ở cạnh dưới.
8. Mở form checkout và nhấn tạo đơn demo bằng dữ liệu giả.
9. Nhấn mạnh đây là UI Foundation: form không gửi đơn thật và không lưu thông tin liên hệ.

## Kịch bản quản trị

1. Mở `/admin.html`.
2. Giới thiệu các nhóm tổng quan, quản lý sách, đơn hàng và báo cáo.
3. Giải thích đây là bản preview giao diện, chưa có đăng nhập hoặc API.

## Kết luận demo

Trình bày cấu trúc repository, dữ liệu catalog JSON, FastAPI static host, kiểm thử và CI. Nêu rõ các chức năng backend là kế hoạch Sprint tiếp theo, không trình bày như chức năng đã hoàn thành.
