# Risk Register — LTD's Book Store

Đánh giá định tính; sau mỗi sprint cập nhật trạng thái và biện pháp xử lý. Không coi một rủi ro đã khép lại chỉ vì có kế hoạch.

| Mã | Rủi ro | Mức | Ảnh hưởng | Ứng phó |
|---|---|---|---|---|
| R01 | ZIP local v1.2.1 khác `main` v0.5.1 | Cao | Nhầm chức năng, release thiếu | PR đồng bộ mã/ảnh + CI trên đúng commit; Issue #10 |
| R02 | Ảnh sản phẩm trên GitHub còn thumbnail nhỏ | Cao | Ảnh mờ, trải nghiệm kém | Nhập ảnh độ phân giải cao từ bản chủ dự án cung cấp; UI test |
| R03 | Mất SQLite và ảnh upload khi thay thư mục | Cao | Mất tài khoản và dữ liệu | Backup `server/data/`, test khôi phục bản sao |
| R04 | Giá/tình trạng sách chưa xác nhận | Cao | Đơn sai, mua sách chưa phát hành | Admin xác nhận giá và trạng thái trước release |
| R05 | Checkout demo nhầm là nhận đơn thật | Cao | Gây hiểu lầm người mua | Ghi giới hạn trong README/UI; chỉ chuyển Done khi có API đã kiểm thử |
| R06 | Lộ `.env`, thông tin đơn/khách | Cao | Rủi ro bảo mật | `.gitignore`, kiểm tra PR/ZIP, che thông tin trong evidence |
| R07 | UI lỗi do cache trình duyệt | Trung bình | Thấy giao diện/ảnh cũ | Versioning asset, hard reload, test Guest và regular |
| R08 | Không có bằng chứng Sprint/Test/PR | Cao | Khó chứng minh đồ án | Evidence theo version và commit; traceability matrix |
| R09 | Scope tăng trước kỳ nộp | Trung bình | Chậm tiến độ | Must/Should/Could, kiểm soát thay đổi mỗi sprint |
| R10 | VPS/HTTPS chưa triển khai | Thấp ở giai đoạn local | Chưa chạy public | Ghi ngoài phạm vi hiện tại, không công bố production |

## Ưu tiên xử lý

**Trước tiên:** R01, R02, R03, R04 và R06. Những hạng mục không có bằng chứng kiểm thử vẫn phải để trạng thái mở trong tracker. Xem [SPRINT-TRACKER.md](SPRINT-TRACKER.md).

## Dấu hiệu và quyết định trong kế hoạch Buổi 9

| Rủi ro | Dấu hiệu để xử lý | Phương án thay thế |
|---|---|---|
| R01 · Lệch phiên bản | VERSION của commit khác ZIP hoặc bản GitHub thiếu route đặt đơn. | Ghi riêng kết quả theo nguồn, giữ mốc Git đã kiểm tra cho đến khi bản đồng bộ qua test. |
| R03 · Mất dữ liệu | Sau phục hồi thiếu đơn mẫu hoặc ảnh đã tải. | Dừng thử trên dữ liệu đang dùng, phục hồi và kiểm tra trên bản sao. |
| R09 · Vượt quỹ giờ | Cuối tuần 2 vẫn chưa có đơn thử tra lại được bằng mã. | Hoãn phần nâng cấp UX, dành giờ tuần 3 cho đặt và theo dõi đơn. |
