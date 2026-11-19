# Triển khai LTD's Book Store

Thư mục này chứa **cấu hình tham khảo**, không phản ánh chắc chắn trạng thái VPS hiện tại.

Trước khi triển khai, cần xác nhận đường dẫn ứng dụng, tài khoản dịch vụ, cổng nội bộ, cấu hình Nginx, chứng chỉ HTTPS và cơ chế sao lưu dữ liệu. Không áp dụng trực tiếp file `math-book-store.service` lên VPS khi chưa đối chiếu service đang chạy.

Kiểm tra `/health`, các trang khách hàng và quản trị, quyền truy cập tệp và dữ liệu đơn hàng trước khi chuyển lưu lượng.

Việc dọn GitHub **không tự triển khai** hoặc thay đổi dữ liệu trên VPS. Chỉ sử dụng thanh toán thực khi đã kiểm chứng tích hợp và luồng giao dịch.
