# Kế hoạch kiểm thử LTD's Book Store

**Phiên bản nguồn GitHub hiện tại:** v0.5.1. Các tính năng có trong ZIP local v0.9.0 **không được coi là đã qua CI trên main** cho tới khi nhập và test. Áp dụng phân loại: **Tự động / Thủ công / Chưa thực hiện**; lưu minh chứng ở [evidence/README.md](evidence/README.md).

## 1. Tự động trên GitHub Actions

- `python -m unittest discover -s tests -v`: FastAPI, dữ liệu, đăng nhập, quyền và API quản trị trong phạm vi test có sẵn.
- `node --check server/web/app.js` và `node --test tests/*.test.cjs`: syntax/cấu trúc catalog và logic frontend được test.
- `python scripts/package.py` và `python scripts/verify_package.py`: xác minh ZIP có đủ ứng dụng, đúng VERSION và không chứa file bí mật / dữ liệu runtime.
- CI chạy trên Ubuntu và Windows. **CI đạt không đồng nghĩa đã kiểm thử toàn bộ giao diện bằng trình duyệt.**

## 2. Ma trận kiểm thử thủ công trước mỗi release

| ID | Luồng | Kết quả mong đợi | Bằng chứng cần |
|---|---|---|---|
| UI01 | Trang chủ desktop 1440px | Không tràn/che nút, ảnh rõ | Screenshot |
| UI02 | Mobile 360/390px, tablet 768px | Header/cart bám đúng, không cuộn ngang | Screenshot |
| UI03 | Tìm kiếm có dấu/không dấu, lọc lớp | Kết quả đúng, trạng thái rỗng rõ | Video/ảnh hoặc checklist |
| UI04 | Mở chi tiết / ảnh sách | Không kéo méo bìa, giá chính xác | Screenshot |
| UI05 | Giỏ: thêm/tăng/giảm/xóa/reload | Tổng tiền và số lượng nhất quán | Checklist |
| UI06 | Sách hết hàng / sắp ra mắt | Có trạng thái, **không cho đặt mua** | Screenshot |
| AUTH01 | Đăng ký, đăng nhập, đăng xuất | Đúng vai trò và cookie phiên | Kết quả test dữ liệu giả |
| AUTH02 | Khách gọi API admin | Trả lỗi phân quyền | API test |
| ADM01 | Thêm/sửa/xóa sách, upload ảnh | API/SQLite lưu đúng, ảnh hiển thị | Screenshot/API test |
| ADM02 | Đổi trạng thái sách | API và UI cùng giá trị | Checklist |
| PKG01 | Khởi động ZIP trên Windows | Có thể đăng nhập vào website local | Log/screenshot |
| ORDER01 | Tạo đơn, lịch sử, hủy đơn, trạng thái | **Chỉ chạy sau khi mã v0.9.0 đã nhập** | API test + screenshot |
| SEC01 | Xem log không lộ secret/PII | Dữ liệu thử nghiệm, có che thông tin | Checklist |

**Ghi chú:** Bảng trên là **test cases cần kiểm tra**, không phải kết quả pass; chỉ đánh dấu đạt sau khi có log hoặc ảnh của đúng phiên bản.

## 3. Cách ghi bằng chứng

Mỗi lần nghiệm thu ghi phiên bản, SHA commit, ngày, OS/trình duyệt, lệnh, các bước, expected/actual, số pass/fail và link PR/Actions. Tên đường dẫn `docs/evidence/vX.Y.Z-YYYY-MM-DD/`. Không sao chép ảnh từ VNU Food Hola làm minh chứng đã kiểm tra LTD.

## 4. Khi test lỗi

Tạo GitHub Issue kèm bước tái hiện, môi trường, mức nghiêm trọng, kết quả dự kiến/thực tế và ảnh đã che PII. Sửa trên `fix/*`, bổ sung regression test, mở PR và chạy lại CI; không tuyên bố đã sửa chỉ vì trang mở được trong một trình duyệt.

## 5. Phạm vi chưa xác minh

- Chức năng đơn hàng / quản lý đơn của ZIP v0.9.0 chưa được kiểm thử trong GitHub `main` v0.5.1.
- Chưa kiểm tra public deployment, thực nhận tiền hay vận chuyển.
- Kiểm thử browser tự động chưa phải bộ chạy mặc định của CI hiện tại.
