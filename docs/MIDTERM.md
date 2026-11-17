# Hồ sơ báo cáo giữa kỳ — LTD's Book Store

Đây là khung báo cáo giữa kỳ dành riêng cho **LTD's Book Store**, không phải tuyên bố dự án đã được chấm hoặc giảng viên đã duyệt.

## 1. Bối cảnh và mục tiêu
- Đề tài: website thương mại điện tử bán sách Toán / sách luyện thi, LTD's Book Store.
- Đối tượng: người mua sách và quản trị viên.
- Phạm vi ưu tiên: website local chạy Windows, ảnh bìa gốc, quản lý sách và đơn hàng khi đã đồng bộ.

## 2. Yêu cầu / phân tích
- Đính kèm [Project Charter](01-project-charter.md), [Requirements](02-requirements.md).
- Ma trận User Story ↔ API/UI ↔ bài test được lập ở [ACADEMIC-TRACEABILITY.md](ACADEMIC-TRACEABILITY.md).

## 3. Thiết kế và triển khai
- Kiến trúc: [03-system-design.md](03-system-design.md).
- Cấu trúc mã nguồn LTD's Book Store: `server/`, `tests/`, `docs/`, `.github/`, `deploy/`.
- Kiểm soát thay đổi: issue → branch → PR → CI Windows/Ubuntu → merge → release.
- Nhận diện: LTD's Book Store; **không tự đổi bìa sách**.

## 4. Tiến độ so với kế hoạch
- [SPRINT-TRACKER.md](SPRINT-TRACKER.md) theo dõi sprint.
- [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md) phân biệt mã GitHub và ZIP local.
- Chỉ ghi công việc đã có bằng chứng thật, đúng nhánh/commit của LTD's Book Store.

## 5. Kiểm thử / minh chứng
- Tự động: liên kết Actions của commit được kiểm tra.
- Thủ công: `docs/evidence/<version>-<date>/`.
- Trường hợp chưa test phải ghi rõ; thông tin cá nhân trong ảnh cần được che.
- Test plan: [TEST-PLAN.md](TEST-PLAN.md).

## 6. Rủi ro và kế hoạch cải thiện
- Chênh lệch nguồn ZIP v0.9.0 và `main` v0.5.1.
- Ảnh thumbnail mờ ở repo cũ; chờ nhập ảnh nét cao.
- Checkout vẫn là demo ở `main`, không nhận đơn thật ở phiên bản này.
- VPS và thanh toán online chưa thuộc phạm vi hiện tại.

## 7. Kết luận chờ điền
- Kết quả trình bày ngày:
- Phiên bản và commit demo:
- Phản hồi giảng viên:
- Mục chưa hoàn thành:
- Kế hoạch sprint tiếp theo:
