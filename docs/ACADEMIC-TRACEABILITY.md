# Ma trận yêu cầu, tài liệu và minh chứng — LTD's Book Store

**Mục đích:** tổng hợp tài liệu và minh chứng kiểm thử của chính LTD's Book Store để báo cáo đồ án có thể kiểm chứng được.

**Cơ sở thực tế:** nhánh `main` LTD's Book Store ở thời điểm soạn hồ sơ đang là **v0.5.1**; bản ZIP local **v0.9.0** chưa nhập đầy đủ vào GitHub. Mọi kết quả kiểm thử phải ghi rõ phiên bản/commit.

## Ma trận hồ sơ

| Phần báo cáo | Tài liệu LTD's Book Store | Minh chứng cần chuẩn bị |
|---|---|---|
| Đề tài & phạm vi | [01-project-charter.md](01-project-charter.md) | Giảng viên duyệt/chỉnh đề tài (nếu có) |
| Yêu cầu / User Story | [02-requirements.md](02-requirements.md) | Bảng đối chiếu US ↔ bài test ↔ ảnh kết quả |
| Kiến trúc & dữ liệu | [03-system-design.md](03-system-design.md) | Sơ đồ thực tế, tên route và bảng database |
| WBS / phân chia việc | [04-wbs.md](04-wbs.md) | Issue/PR liên kết với sản phẩm bàn giao |
| Gantt và tiến độ | [05-schedule.md](05-schedule.md) | Ngày thật, thời lượng dự kiến/thực tế |
| Scrum / vai trò | [06-scrum-team.md](06-scrum-team.md) | Phân vai đúng người thực hiện, sprint review |
| Sprint Backlog | [07-sprint-0-backlog.md](07-sprint-0-backlog.md), [SPRINT-TRACKER.md](SPRINT-TRACKER.md) | Issue ↔ nhánh ↔ PR ↔ commit |
| Demo & nghiệm thu | [08-mvp-demo.md](08-mvp-demo.md), [evidence/README.md](evidence/README.md) | Ảnh desktop/mobile, kết quả test, hạn chế |
| Chất lượng và rủi ro | [QUALITY.md](QUALITY.md), [RISKS.md](RISKS.md) | Danh sách lỗi, kiểm thử lại, rủi ro |
| Git và phát hành | [GIT.md](GIT.md), [VERSIONING.md](VERSIONING.md), [WORKFLOW.md](WORKFLOW.md) | CI xanh trên commit, PR review, release tương ứng |
| Báo cáo / bàn giao | [FINAL-REPORT.md](FINAL-REPORT.md), [FINAL-HANDOVER.md](FINAL-HANDOVER.md) | Checklist đối chiếu đã làm/chưa làm |

## Ma trận chức năng / trạng thái thật trên GitHub

| Nhóm | Nhánh `main` v0.5.1 | Bằng chứng mong đợi |
|---|---|---|
| Catalog, tìm kiếm, giỏ demo | Có mã giao diện | Ảnh mobile/desktop, bước chạy thử, test JS |
| Đăng ký và đăng nhập | Có route API và trang | Test sai mật khẩu, phân quyền, cookie |
| Thêm/sửa/xóa sách và tải bìa | Có API và UI | Test CRUD, kiểm tra ảnh đã lưu |
| Còn hàng, hết hàng, sắp ra mắt | Có status trong dữ liệu | Test không mua sách chưa bán |
| Thanh toán/đơn hàng thực | **Chưa nằm trên main v0.5.1** | Chỉ đánh dấu Done sau khi nhập ZIP, test API+UI |
| Ảnh sách 3D nét cao | **Chưa nhập đủ vào main** | Kích thước ảnh, ảnh chụp UI, tải trang |
| VPS production | **Không thuộc giai đoạn này** | Không ghi nhận như đã triển khai |

**Quy tắc chấm minh chứng:** không đánh dấu hoàn thành chỉ vì có file tên tương ứng, bài test trên bản khác, ảnh demo giả hoặc CI của commit cũ; chỉ dùng kết quả xác thực được.

## Thứ tự chuẩn bị buổi bảo vệ

1. Trình bày Charter → User Story/ưu tiên → WBS/Sprint → thiết kế và công nghệ.
2. Chạy demo từ phiên bản/tag cố định: xem sách, lọc, giỏ, tài khoản, quản trị và đơn hàng **nếu mã đã đồng bộ**.
3. Đưa ảnh chụp **GitHub Issues → PR → CI → tag/release**, giải thích ít nhất một lần sửa lỗi có kiểm thử lại.
4. Đối chiếu từng chức năng với `tests/` và biên bản thủ công; nêu rõ mục chưa làm (thanh toán trực tuyến, VPS).
5. Trình bày bài học kỹ thuật và kế hoạch cải thiện; không khẳng định điểm số hoặc nghiệm thu khi chưa có phản hồi từ giảng viên.
