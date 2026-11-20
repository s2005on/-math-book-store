# 04 — Work Breakdown Structure

**Mốc hiện hành:** v1.3.0 Pro Edition. Các bảng v0.5.1 bên dưới là ghi nhận lịch sử. [Đối chiếu nguồn và phiên bản](REPO-SYNC-STATUS.md) · [Nghiệm thu Buổi 9](B9.md).

| WBS | Công việc | Kết quả | Trạng thái |
|---|---|---|---|
| 1.0 | Khởi tạo dự án | Repository, README, Git ignore | Hoàn thành |
| 1.1 | Phân tích yêu cầu | Project charter, user stories | Hoàn thành bản đầu |
| 1.2 | Thiết kế UI | Design system, responsive layout | Hoàn thành bản đầu |
| 1.3 | Xử lý ảnh sản phẩm | Bộ mockup bìa sách | Hoàn thành 7 sản phẩm |
| 1.4 | Storefront | Catalog, search, filter, detail | Hoàn thành UI |
| 1.5 | Cart demo | Cart drawer, quantity, total | Hoàn thành demo |
| 1.6 | Admin preview | Dashboard tĩnh | Hoàn thành UI |
| 1.7 | Test và CI | Python/Node checks, GitHub Actions | Hoàn thành bản đầu |
| 2.0 | Catalog API + database | CRUD sách | Có trong `main` v0.5.1; cần bằng chứng cập nhật |
| 2.1 | Admin authentication | Đăng nhập, phân quyền | Có trong `main` v0.5.1; cần bằng chứng cập nhật |
| 3.0 | Order API | Tạo và tra cứu đơn | Có trong ZIP local v0.9.0; chưa lên `main` |
| 4.0 | Release hardening | Security, backup, deploy, acceptance | CI/ZIP có trên `main`; VPS tạm hoãn |

> Trạng thái trên dựa vào mã GitHub và sự khác biệt với ZIP local; để đánh dấu **đã nghiệm thu** cần evidence và kiểm thử của đúng commit. Theo dõi [SPRINT-TRACKER.md](SPRINT-TRACKER.md).
