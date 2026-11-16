# Sprint tracker — LTD's Book Store

Tham chiếu mô hình Scrum rút gọn của VNU Food Hola: **mục tiêu → backlog/issue → nhánh/PR → test → demo → retrospective**. Với đồ án cá nhân, các vai trò có thể kiêm nhiệm; người thực hiện/giảng viên điền sau khi xác nhận.

## Lịch theo mốc, chưa ấn định hạn nộp

| Giai đoạn | Kết quả cần đạt | Ưu tiên | Trạng thái thực tế |
|---|---|---|---|
| Sprint 0 — Nền tảng | Repo, UI cơ bản, tài liệu 01–08, CI | Must | Có hồ sơ lịch sử, xem [SPRINT0-REPORT.md](SPRINT0-REPORT.md) |
| Sprint 1 — Catalog + auth | SQLite sách, login, CRUD admin, trạng thái | Must | Có mã trong `main` v0.5.1, cần làm mới minh chứng |
| Sprint 2 — Hoàn thiện bán sách | Đơn hàng, trạng thái, ảnh sắc nét, banner | Must | Có trong ZIP local v0.9.0, **chưa đồng bộ main**; theo dõi [Issue #3](https://github.com/s2005on/LTDs-Book-Store/issues/3) |
| Sprint 3 — Kiểm thử & bàn giao | Regression, responsive, tài liệu, ZIP, release | Must | Đang hoàn thiện quy trình; chưa có Release v0.9.0 |
| VPS | Triển khai công khai | Could | Tạm hoãn theo quyết định hiện tại |

## Kanban: To do / Doing / Done

- **To do:** nhận ZIP v0.9.0 vào nhánh riêng, kiểm tra diff, nhập ảnh sách và order API, kiểm thử end-to-end; chuẩn bị ảnh minh chứng; đối chiếu yêu cầu giảng viên.
- **Doing:** chuẩn hóa quy trình hồ sơ minh chứng và tiếp nhận release, đưa thay đổi qua PR.
- **Done:** repo đã đổi tên LTDs, cấu trúc tài liệu 01–08, CI Windows/Ubuntu kiểm tra Python/Node và gói ZIP từ VERSION.

Mỗi khi chuyển trạng thái, cập nhật link Issue/PR và ghi ngày, không tự đánh dấu hoàn thành nếu chưa có bằng chứng.

## Mẫu nhật ký buổi làm việc

| Ngày | Mục tiêu | Việc đã làm | Khó khăn | Link Issue/PR/test | Việc tiếp theo |
|---|---|---|---|---|---|
| (điền khi thực hiện) | | | | | |

## Sprint review / retrospective

- Bản dùng để demo: tên ZIP + SHA commit/tag.
- Chức năng demo đạt/chưa đạt: liệt kê cụ thể.
- Minh chứng: link `docs/evidence/<version>-<date>/`.
- Phản hồi của giảng viên (nếu có): ghi nguyên nội dung, ngày nhận.
- Điểm cần cải thiện: một việc kỹ thuật + một việc quản lý.
