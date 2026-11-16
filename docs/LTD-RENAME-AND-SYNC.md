# Xác nhận đổi tên và đồng bộ LTD's Book Store v0.9.0

**Tên hiển thị:** LTD's Book Store  
**Repository chính thức:** [s2005on/LTDs-Book-Store](https://github.com/s2005on/LTDs-Book-Store)  
**Trạng thái tên repo:** Đã đổi tên thành công và đã xác minh quyền ghi trên GitHub. Không cần đổi tên lại.

## Đã hoàn tất
- Repository vẫn giữ lịch sử Git, Pull Request và Issues.
- Nhận diện LTD's Book Store trong phần frontend/backend hiện có trên `main`.
- Quy trình branch/PR/CI Windows + Ubuntu và đóng gói ZIP theo phiên bản.
- Bản ZIP chuẩn hóa `LTDs-Book-Store-v0.9.0` đã được kiểm thử tại máy làm việc: **16 Python tests + 4 JavaScript tests đạt**. Đây là kiểm thử mã trong ZIP, chưa phải CI của commit `main` v0.9.0.

## Phần CHƯA đồng bộ vào main
`main` hiện có `VERSION=0.5.1` và một số ảnh thumbnail rất nhỏ. ZIP v0.9.0 có các chức năng quản lý đơn hàng và ảnh bìa WebP nét cao, cùng `anh-goc` là các tệp ảnh gốc; **chưa thể gọi mã GitHub là v0.9.0 cho đến khi toàn bộ được nhập và CI đạt**.

## Nhập ZIP v0.9.0 lên repo mới, giữ lịch sử Git

Bản ZIP đã chuẩn hóa có công cụ `IMPORT-LTD-GITHUB.bat`. Thao tác trên Windows:

1. Cài **Git for Windows**, đăng nhập GitHub để có quyền push repo.
2. Giải nén ZIP, mở thư mục `LTDs-Book-Store`, nhấn đúp **`IMPORT-LTD-GITHUB.bat`**.
3. Công cụ clone `https://github.com/s2005on/LTDs-Book-Store.git`, tạo nhánh riêng `feat/import-ltd-v0.9.0-...`, sao chép tệp ứng dụng/ảnh và push.
4. Nhấn **Create pull request** trên trang được tự mở, kiểm tra **Files changed** trước khi merge.
5. Đợi CI **Windows + Ubuntu** đạt. Kiểm tra lần cuối rằng giá HSG Toán 8 là **198.000đ**, sách Toán tổ hợp và tư duy logic là **280.000đ** và **sắp ra mắt** (không thể mua).
6. Khi CI xanh và PR được nhập vào `main`, kiểm tra `VERSION=0.9.0` và nội dung ZIP trước khi gắn tag/release `v0.9.0`.

Công cụ nhập **không sửa `main` ngay**, chỉ đẩy nhánh mới để review. Nó giữ lại thư mục `.github/`, `docs/` và quy trình phát hành đã có trên repo.

## Bảo vệ dữ liệu
- Tuyệt đối không commit `.env`, `.venv`, `server/data/`, SQLite có khách hàng, mật khẩu, đơn hàng, hoặc cache Python.
- Không đẩy các thay đổi nhạy cảm trước khi xem diff.
- Giữ nguyên thiết kế bìa gốc, chỉ nâng độ phân giải hiển thị.
- COD/VietQR/MoMo/VNPAY trong đồ án là **mô phỏng**, chưa tích hợp thanh toán thực.
- Chưa triển khai VPS; phạm vi hiện tại là chạy local Windows.

Theo dõi tiến độ nhập mã nguồn và ảnh: [Issue #3](https://github.com/s2005on/LTDs-Book-Store/issues/3).
