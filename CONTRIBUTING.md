# Đóng góp và quy trình làm việc

- Tạo nhánh `feat/*`, `fix/*`, `docs/*`, `test/*`; không làm trực tiếp trên main.
- Mỗi PR cần mô tả mục tiêu, phạm vi, ảnh hưởng và cách kiểm thử.
- Chạy trước khi push:
```bash
python -m unittest discover -s tests -v
node --test tests/*.test.cjs
```
- Cập nhật CHANGELOG và tài liệu liên quan.
- Không commit secrets, dữ liệu khách hàng, file môi trường hoặc database runtime.
- Không coi checkout demo là đơn hàng production.
