# Đóng góp cho LTD's Book Store

Mã nguồn chính là nhánh `main`. Để giữ lịch sử phát triển rõ ràng và hỗ trợ nghiệm thu đồ án, **không commit trực tiếp lên `main`** khi thay đổi tính năng, ảnh hoặc tài liệu.

## 1. Quy trình theo Issue và Pull Request

1. Mở [Issue](https://github.com/s2005on/LTDs-Book-Store/issues) ghi mục tiêu, bước tái hiện lỗi hoặc User Story, tiêu chí chấp nhận.
2. Tạo nhánh từ `main`: `feat/*`, `fix/*`, `docs/*`, `test/*` hoặc `chore/*`.
3. Thực hiện một thay đổi có phạm vi rõ; thêm/sửa test và tài liệu nếu cần.
4. Tạo Pull Request, điền đúng [PR template](.github/PULL_REQUEST_TEMPLATE.md).
5. Kiểm tra `Files changed`, CI Ubuntu/Windows, ảnh minh chứng giao diện (nếu có thay đổi UI).
6. Chỉ merge sau khi đạt yêu cầu; khi release, VERSION và CHANGELOG phải trùng tag và ZIP.

## 2. Các lệnh kiểm thử

```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -v
node --check server/web/app.js
node --test tests/*.test.cjs
python scripts/package.py
python scripts/verify_package.py
```

CI tự chạy kiểm thử Python/JavaScript và xác minh ZIP. Với thay đổi giao diện, cần kiểm tra thủ công desktop/mobile và lưu bằng chứng tại [docs/evidence/](docs/evidence/README.md).

## 3. Quy tắc commit

| Tiền tố | Khi sử dụng |
|---|---|
| `feat:` | Thêm chức năng |
| `fix:` | Sửa lỗi |
| `docs:` | Cập nhật tài liệu |
| `test:` | Kiểm thử |
| `refactor:` | Tái cấu trúc mà không thay hành vi |
| `chore:` | Công việc bảo trì, công cụ |

Ví dụ: `fix(auth): validate phone number on registration`. Gắn Issue/PR khi có thể.

## 4. Tiếp nhận ZIP từ chủ dự án

- Ghi tên ZIP, `VERSION` bên trong và SHA-256, so sánh với `main`.
- Nhập code, ảnh và test vào nhánh riêng. Không ghi đè `.github/`, `docs/` hay `scripts/` từ những bản ZIP cũ.
- Kiểm thử migration với cơ sở dữ liệu giả và sao lưu `server/data/` trên máy trước khi nâng cấp.
- **Không coi bản ZIP local là phiên bản GitHub** cho tới khi PR được merge và CI chạy trên đúng commit.
- Xem [VERSION-INTAKE.md](docs/VERSION-INTAKE.md) và [REPO-SYNC-STATUS.md](docs/REPO-SYNC-STATUS.md).

## 5. An toàn dữ liệu

Không đưa lên GitHub: `.env`, `.venv/`, `server/data/`, file `.sqlite3`, ảnh có thông tin cá nhân, token, mật khẩu, database khách/đơn thật hay backup. Giữ nguyên nội dung bìa sách được cung cấp; chỉ chỉnh cách hiển thị ảnh khi cần.

Hiện dự án ưu tiên **đồ án demo local**, chưa có thanh toán online hoặc VPS production.
