# B2 — Báo cáo kỹ thuật và bằng chứng (khung dành cho LTD's Book Store)

Báo cáo B2 của **LTD's Book Store** chỉ trình bày kết quả của dự án này. Mọi ảnh, log và kết quả kiểm thử phải phản ánh đúng phiên bản, commit và quá trình thực hiện.

## 1. Môi trường dự án

- Repository: https://github.com/s2005on/LTDs-Book-Store
- Ngôn ngữ: HTML/CSS/JavaScript (frontend); Python/FastAPI (backend), SQLite (lưu dữ liệu).
- Chạy local Windows: `RUN-WINDOWS.bat`, Python 3.11+, ứng dụng tại `127.0.0.1:8017`.
- CI: GitHub Actions trên Windows và Ubuntu, chạy Python tests, JavaScript tests và kiểm tra ZIP.

## 2. Minh chứng cần thu thập

| Bằng chứng | Mục đích | Trạng thái |
|---|---|---|
| `01-setup.png` | Môi trường Python đã cài, không lộ username/mật khẩu | Chưa đưa lên repo |
| `02-health.png` | FastAPI `/health` trả dữ liệu đúng | Chưa đưa lên repo |
| `03-home.png` | Trang cửa hàng trên desktop | Chưa đưa lên repo |
| `04-admin.png` | Trang quản trị hoạt động với tài khoản giả | Chưa đưa lên repo |
| `05-ci.png` | CI cho đúng commit; có thể dẫn link Actions thay screenshot | Chưa đưa lên repo |
| `06-test-log.txt` | Lệnh test và kết quả thực tế, có version/commit | Chưa đưa lên repo |

Ảnh/log thật sẽ đặt trong `docs/evidence/<version>-<date>/`. Không lưu ảnh demo lấy từ internet như bằng chứng đã chạy.

## 3. Kết quả cần trình bày

- Kiến trúc và tên route **thực có**: [03-system-design.md](03-system-design.md).
- Tài liệu đo lường chất lượng: [QUALITY.md](QUALITY.md), [TEST-PLAN.md](TEST-PLAN.md).
- Link Issue/PR/CI và commit đúng bản.
- Những hạn chế cần nêu: `main` chưa có order backend và ảnh nét cao của ZIP local v0.9.0; chưa VPS/production.

## 4. Kết luận chờ cập nhật sau demo

- Ngày demo, commit/tag:
- Test pass/fail cụ thể:
- Điều đạt và chưa đạt:
- Phản hồi của giảng viên:
- Sprint tiếp theo:
