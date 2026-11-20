# LTD's Book Store — Phiên bản v1.3.0 (Artaka Pro Operations & Workflow Edition)

## 1. Tinh gọn các điểm thừa & bất cập quy trình cũ
- **Hợp nhất thanh tìm kiếm thông minh**: Lược bỏ sự chồng chéo của 2 thanh tìm kiếm trên màn hình máy tính, tích hợp **Gợi ý tức thì (Live Search Autocomplete)** ngay trên thanh Header (hỗ trợ phím tắt `/`, hiển thị ảnh bìa, lớp học và giá bán).
- **Tinh gọn hộp thoại Thanh toán**: Loại bỏ ô nhập mã giảm giá bị lặp lần 2; bổ sung **Bảng kê chi tiết sách đang đặt** kèm nút quay lại sửa giỏ hàng nhanh và bảng tách bạch *Tạm tính – Phí vận chuyển – Ưu đãi – Tổng thanh toán*.
- **Liền mạch luồng Đăng ký → Mua hàng**: Đăng ký tài khoản xong tự động đăng nhập phiên ngay lập tức (không bắt gõ lại mật khẩu) và tự động điền sẵn **Họ tên, Số điện thoại, Địa chỉ giao hàng mặc định** vào biểu mẫu thanh toán.
- **Đồng bộ hóa Freeship thực tế & dọn CSS thừa**: Biến thanh tiến trình Freeship thành nghiệp vụ tính phí vận chuyển thực sự (tùy chỉnh được trong Quản trị); dọn dẹp các khối CSS cũ không còn dùng và đồng bộ `admin.css` làm stylesheet chính thức cho `admin.html`.

## 2. Chức năng mới cho Khách hàng & Tài khoản (`index.html`, `account.html`)
- **Mua ngay 1 chạm (`⚡`)**: Chốt nhanh đầu sách đang xem và mở thẳng bước xác nhận đơn đã điền sẵn thông tin người nhận.
- **Bộ lọc chuyên sâu & Sách vừa xem**: Lọc kết hợp theo **Mục tiêu lộ trình**, **Khoảng giá**, **Chỉ hiện còn hàng**, sắp xếp theo **Đánh giá cao nhất**, và lưu lịch sử **Sách bạn vừa xem**.
- **Đánh giá sách xác thực (`1–5 ★`) & Gợi ý mua kèm**: Xem/gửi nhận xét sao (tự động gắn nhãn `✓ Đã mua sách` nếu tài khoản từng đặt mua) và gợi ý đầu sách cùng khối lớp ngay trong cửa sổ chi tiết.
- **Đăng ký chờ Sách sắp ra mắt (Waitlist)**: Cho phép học sinh/phụ huynh để lại tên & SĐT nhận thông báo ngay khi đầu sách mới phát hành.
- **Trung tâm Tài khoản nâng cấp**: Sửa hồ sơ & địa chỉ nhận hàng mặc định, đổi mật khẩu, theo dõi **Thanh tiến trình đơn hàng 4 bước**, xem **Mã vận đơn & Ghi chú từ shop**, bấm **Mua lại đơn cũ 1 chạm** và **In phiếu đơn hàng**.

## 3. Hệ thống Quản trị & Vận hành hiện đại (`admin.html`, `server/app.py`)
- **Quản trị tồn kho tự động (`stock_qty`)**: Tự động trừ tồn kho khi khách đặt sách, tự chuyển `Hết hàng` khi về `0`, **tự động hoàn lại kho khi khách hoặc Admin hủy đơn**, cảnh báo `Sắp hết kho (≤ 5 cuốn)` và nút nhập nhanh `+10 kho`.
- **Kho ảnh bìa linh hoạt**: Cho phép chọn lại ngay ảnh có sẵn trong thư viện máy chủ hoặc tải ảnh bìa mới, kèm tùy chỉnh thứ tự ưu tiên (`sortOrder`).
- **Xử lý Vận đơn chuyên nghiệp**: Tìm kiếm đơn hàng theo mã đơn/tên/SĐT, nút duyệt nhanh 1 chạm (*Xác nhận → Giao vận chuyển → Hoàn tất*), gắn **Mã vận đơn** & **Ghi chú shop**, **In phiếu giao hàng (Packing Slip)** và **Xuất báo cáo đơn hàng ra CSV (`/api/admin/orders/export.csv`)**.
- **CRM & Phân tích kinh doanh**: Thống kê **Top đầu sách bán chạy nhất**, tỷ trọng kênh thanh toán, danh sách **Khách hàng thành viên** (tổng chi tiêu), danh sách **Khách chờ sách sắp mở bán** và kiểm duyệt **Đánh giá độc giả**.
