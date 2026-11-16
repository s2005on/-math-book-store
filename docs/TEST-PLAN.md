# 05 — Kế hoạch kiểm thử

## Phạm vi kiểm thử hiện tại

- Dữ liệu catalog đúng cấu trúc và không trùng ID.
- Giá có dạng số dương hoặc `null`.
- Tất cả đường dẫn ảnh trong catalog tồn tại.
- Ảnh được tham chiếu từ UI đúng tên file.
- FastAPI trả health status và phục vụ trang chủ.
- Node kiểm tra dữ liệu catalog và asset references.

## Kiểm thử thủ công UI

1. Mở trang trên desktop, tablet và điện thoại.
2. Cuộn trang để kiểm tra header sticky và thanh giỏ hàng.
3. Tìm kiếm bằng từ khóa có dấu và không dấu.
4. Lọc theo từng lớp, reset bộ lọc và sắp xếp giá.
5. Mở chi tiết sách, thêm vào giỏ, tăng/giảm số lượng, xóa sản phẩm.
6. Tải lại trang để kiểm tra giỏ hàng còn nguyên trên cùng trình duyệt.
7. Thử checkout bằng dữ liệu giả; xác nhận chỉ hiện thông báo demo.
8. Kiểm tra sản phẩm chưa có giá không thể thêm vào giỏ.
9. Kiểm tra admin preview và nhãn dữ liệu minh họa.

## Chưa kiểm thử

Chưa có API đơn hàng, database, đăng nhập, thanh toán và quản lý tồn kho; các nội dung này không thuộc phạm vi nghiệm thu Sprint 0.
