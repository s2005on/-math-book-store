# Quy ước Git — Math Book Store

- `main`: nhánh tích hợp ổn định. Đề nghị cập nhật qua PR, không sửa trực tiếp.
- Nhánh công việc: `feat/*`, `fix/*`, `docs/*`, `test/*`, `chore/*`.
- Commit: `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`.
- PR ghi mục tiêu, file thay đổi, test, rủi ro và minh chứng giao diện; xem diff và CI trước merge.
- Tag theo SemVer phải trỏ vào commit đã kiểm tra trên `main`. Không sửa tag đã công bố.
- Không đưa `.env`, SQLite, `server/data/`, mật khẩu hoặc dữ liệu khách lên repo.

Quy trình chi tiết: [WORKFLOW.md](WORKFLOW.md). Chênh lệch phiên bản ZIP và repo: [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md).
