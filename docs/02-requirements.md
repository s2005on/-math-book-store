# 02 — Yêu cầu hệ thống và phạm vi

## Vai trò người dùng

- **Khách hàng:** duyệt danh mục, xem chi tiết, thêm sách vào giỏ và ở giai đoạn sau đặt/tra cứu đơn.
- **Quản trị viên:** ở giai đoạn sau đăng nhập, quản lý sản phẩm và đơn hàng.

## User Stories

| Mã | User Story | Ưu tiên | Trạng thái |
|---|---|---|---|
| US01 | Là khách hàng, tôi muốn xem ảnh bìa, tên và giá sách để lựa chọn. | Must | UI có |
| US02 | Tôi muốn lọc sách theo lớp học để tìm nhanh. | Must | UI có |
| US03 | Tôi muốn tìm kiếm và sắp xếp danh mục. | Should | UI có |
| US04 | Tôi muốn xem thông tin chi tiết một sản phẩm. | Must | UI có |
| US05 | Tôi muốn thêm, xóa và đổi số lượng trong giỏ. | Must | Demo có |
| US06 | Tôi muốn gửi đơn và nhận mã đơn. | Must | Chưa có backend; form demo |
| US07 | Quản trị viên muốn đăng nhập để quản lý hệ thống. | Must | Chưa triển khai |
| US08 | Quản trị viên muốn thêm, sửa, ẩn sản phẩm và cập nhật giá. | Must | Admin UI preview |
| US09 | Quản trị viên muốn xem và cập nhật trạng thái đơn hàng. | Must | Chưa triển khai |
| US10 | Người mua muốn thanh toán trực tuyến. | Could | Ngoài phạm vi Sprint 0 |

## Quy tắc nghiệp vụ cần áp dụng ở Sprint backend

- Chỉ sản phẩm đang bán và còn hàng mới được đặt.
- Số lượng là số nguyên dương và có giới hạn cấu hình.
- Backend phải tự tính tổng tiền từ giá trong database.
- Lưu snapshot tên, giá và số lượng tại thời điểm đặt.
- Không xác nhận đơn trước khi giao dịch database hoàn tất.
- Đơn hàng phải có mã khó đoán và thông tin tra cứu riêng tư.
- API quản trị phải yêu cầu xác thực và phân quyền.

## Yêu cầu phi chức năng

- Responsive và hỗ trợ bàn phím cơ bản.
- Có trạng thái rỗng, thông báo lỗi và thông báo thao tác.
- Không đưa secret vào repository.
- Không lưu thông tin liên hệ thật ở frontend demo.
- Bản production phải dùng HTTPS, backup và kiểm tra dữ liệu phía server.
