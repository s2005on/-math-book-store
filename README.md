# Math Book Store v0.3.0

Website demo bán sách tham khảo Toán lớp 6–9 và tài liệu ôn thi vào lớp 10. Dự án độc lập, tham khảo cấu trúc tổ chức repository và luồng mua hàng của [VNU Food Hola](https://github.com/s2005on/vnu-food-hola), không sao chép giao diện hay mã nguồn.

## Giao diện và chức năng
- Nhận diện riêng tông xanh navy – kem – đồng, phong cách cửa hàng sách.
- Header điều hướng cố định khi cuộn, responsive trên điện thoại.
- Danh mục sách theo lớp, tìm kiếm tiếng Việt không dấu, lọc và sắp xếp.
- Thẻ sản phẩm, xem chi tiết, giỏ hàng, thay đổi số lượng và tổng tiền.
- Giỏ hàng lưu trong localStorage; biểu mẫu checkout chỉ tạo đơn demo.
- Ảnh mockup sách dạng cuốn; giữ nguyên thiết kế bìa sách gốc.
- FastAPI static host, health endpoint, trang admin preview, CI và tài liệu đồ án.

## Chạy local
Yêu cầu Python 3.11+.

Windows: chạy `RUN-WINDOWS.bat`, sau đó mở http://127.0.0.1:8017/

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r server/requirements.txt
python -m uvicorn server.app:app --host 127.0.0.1 --port 8017
```

## Kiểm thử
```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -v
node --check server/web/app.js
node --test tests/*.test.cjs
```

## GitHub Pages
Workflow `.github/workflows/pages.yml` xuất bản thư mục `server/web`. Trong Settings → Pages, chọn Build and deployment → Source: GitHub Actions. GitHub Pages chỉ chạy giao diện tĩnh; API `/health` chỉ có trên FastAPI/VPS.

## Giới hạn bản demo
Checkout không gửi hoặc lưu đơn hàng ở máy chủ. Chưa có database, API đơn hàng, đăng nhập admin, thanh toán hoặc xử lý đơn thật. Không nhập dữ liệu cá nhân thật vào bản demo. Trước khi kinh doanh cần hoàn thiện backend, bảo mật, HTTPS, lưu trữ và quy trình vận hành.

## Triển khai VPS
Xem `deploy/README.md`. Cần quyền truy cập VPS và cấu hình domain/HTTPS để triển khai thật. Website VNU Food Hola không bị chỉnh sửa.

## Giá tham khảo
- Bài tập thực hành Toán 6–9, bộ 2 tập: 80.000đ/bộ.
- Luyện thi vào lớp 10 – Đại số & Hình học: 270.000đ/bộ.
- Chinh phục đề thi học sinh giỏi Toán 8: 198.000đ.
- 63 đề ôn thi vào lớp 10: chưa xác nhận giá.

Giá là dữ liệu mẫu từ thông tin người bán đã cung cấp, cần xác nhận trước khi sử dụng thương mại.
