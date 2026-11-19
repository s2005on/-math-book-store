# LTD's Book Store

Website bán sách tham khảo Toán lớp 6–9 và tài liệu ôn thi vào lớp 10.

## Trạng thái mã nguồn

Nhánh `main` hiện chứa phiên bản **0.5.1**. Bản **1.3.0 Pro Edition** được phát triển riêng và chưa được nhập đầy đủ vào repository. Không sử dụng `VERSION` trên `main` để suy ra phiên bản đang chạy trên VPS.

## Chạy trên máy

Yêu cầu Python 3.11 trở lên.

- Windows: chạy `RUN-WINDOWS.bat`.
- Linux/macOS: chạy `./run.sh`.
- Mặc định truy cập `http://127.0.0.1:8017/`.
- Dữ liệu ứng dụng được lưu trong `server/data/`; sao lưu trước khi nâng cấp.

## Kiểm thử

```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -v
node --check server/web/app.js
node --test tests/*.test.cjs
```

## Cấu trúc

- `server/`: FastAPI, giao diện và tài nguyên.
- `tests/`: kiểm thử tự động.
- `deploy/`: cấu hình triển khai tham khảo.
- `docs/`: tài liệu kỹ thuật, kiểm thử và hồ sơ học phần.
- `.github/workflows/`: kiểm thử và quy trình phát hành.

## Phát triển

Thay đổi mã nguồn qua nhánh riêng và Pull Request. Kiểm tra CI trước khi merge. Không đưa `.env`, cơ sở dữ liệu, tài khoản hoặc dữ liệu khách hàng lên GitHub.

Chỉ phát hành khi mã nguồn, kiểm thử và phiên bản đã được xác nhận. Việc nhập v1.3.0 không tự động tạo tag hoặc GitHub Release.

Tài liệu chi tiết: [Hướng dẫn sử dụng](START-HERE.md) · [Quy ước Git](docs/GIT.md) · [Kiểm thử](docs/TEST-PLAN.md) · [Trạng thái đồng bộ](docs/REPO-SYNC-STATUS.md).
