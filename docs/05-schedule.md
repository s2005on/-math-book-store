# Kế hoạch cá nhân 4 tuần

Bản đề xuất cho Buổi 9. Tuần 1 bắt đầu khi sinh viên triển khai kế hoạch. Quỹ 36 giờ dưới đây là ước lượng để điều chỉnh theo lịch học. Hạn nộp theo LMS. Mốc xuất phát và tiêu chí của từng user story nằm trong [hồ sơ B9](B9.md).

| Tuần | Công việc và giờ dự kiến | Phụ thuộc | Đầu ra để kiểm tra |
|---|---|---|---|
| 1 · 8 giờ | W1.1 Rà phạm vi, nguồn và tiêu chí (3h). W1.2 Đối chiếu mã, dữ liệu và chạy thử API (3h). W1.3 Trao đổi theo cặp và điều chỉnh kế hoạch (2h). | Cần bản nguồn và dữ liệu sách mẫu. W1.3 dùng kết quả hai việc đầu. | Danh sách story cốt lõi, sơ đồ dữ liệu, kết quả thử có phiên bản. Ghi góp ý thật và lý do nhận hoặc hoãn. |
| 2 · 10 giờ | W2.1 Đồng bộ bản Pro và kiểm tra ảnh, cấu hình (4h). W2.2 Kiểm tra tìm sách, giỏ, gửi đơn và truy xuất đơn (4h). W2.3 Sửa lỗi cản trở đặt hàng (2h). | Dùng tiêu chí W1.1 và bộ test W1.2. Kiểm tra trên đúng commit sau W2.1. | Từ bản tải trên GitHub, khách đặt được sách còn hàng, nhận mã, mở lại tài khoản thấy đơn và tổng tiền đúng. |
| 3 · 9 giờ | W3.1 Kiểm tra quản trị cập nhật đơn và tồn kho (3h). W3.2 Mời một bạn cùng lớp thử mua sách trên điện thoại và máy tính (2h). W3.3 Sửa và kiểm tra lại lỗi ưu tiên (4h). | Có bản chạy được từ tuần 2. W3.3 dựa vào kết quả W3.1–2. | Lưu mã ca thử, thiết bị, kết quả thực tế, góp ý, lỗi và kết quả thử lại. Người dùng thử dự kiến, chờ xác nhận. |
| 4 · 9 giờ | W4.1 Cài lại bản demo trên máy sạch, chạy hồi quy (3h). W4.2 Viết báo cáo và dẫn link minh chứng (3h). W4.3 Diễn tập, nghiệm thu và chốt commit (3h). | Bản đã xử lý lỗi tuần 3. Chốt commit sau hồi quy. | Hướng dẫn chạy lại được, log theo commit, báo cáo, bài trình bày, link repo và commit nộp LMS. |

Sau mỗi tuần, sinh viên ghi ngày thực hiện, giờ thực tế, sản phẩm và việc chuyển tiếp theo lịch sử Git. Bắt đầu bằng [WBS](04-wbs.md) và ghi tiến độ tại [Sprint Tracker](SPRINT-TRACKER.md).

## Mốc sprint đã ghi trước Buổi 9

| Phase | Work | Output | Status |
|---|---|---|---|
| Sprint 0 | UI, catalog, cart demo, docs, CI | UI Foundation v0.2.0 | Hồ sơ lịch sử đã có |
| Sprint 1 | Database, catalog API, admin auth | Admin/catalog MVP | Có mã trong GitHub v0.5.1, cần evidence |
| Sprint 2 | Checkout API, order lifecycle | Order management | ZIP v0.9.0 local; chờ nhập GitHub |
| Sprint 3 | Security, regression, handover | Academic final release | Chờ kiểm thử và hồ sơ; VPS tạm hoãn |

Dates and sprint duration must be aligned with the lecturer's submission calendar. Do not report planned work as completed.

**Lưu ý:** Đây là mốc công việc tương đối, không phải Gantt theo ngày hoặc lời khẳng định thời gian đã sử dụng. Ngày bắt đầu/hạn nộp chính thức cần người thực hiện/giảng viên xác nhận. Tiến độ và backlink Issue/PR được cập nhật tại [SPRINT-TRACKER.md](SPRINT-TRACKER.md); không ghi mốc giả để đủ tài liệu.
