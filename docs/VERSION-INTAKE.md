# Quy trình tiếp nhận phiên bản ZIP do chủ dự án gửi

Mỗi lần nhận bản ZIP mới, xử lý như một **đầu vào cần kiểm định**, không phải mặc nhiên là mã nguồn chính thức. Repo GitHub `main` và gói chạy Windows có thể khác phiên bản.

## Biểu mẫu một phiên bản

| Mục | Ghi chú cần điền |
|---|---|
| Tệp ZIP và số phiên bản | Tên chính xác, ví dụ `LTDs-Book-Store-v0.9.0.zip` |
| SHA-256 ZIP | Ghi hàm băm tệp thực tế |
| Ngày nhận, nguồn | Ngày gửi và nguồn tệp; không ghi dữ liệu riêng tư |
| Mã nguồn nền | SHA `main` tại thời điểm nhận |
| Nhánh làm việc | `feat/import-vX.Y.Z` hoặc `fix/...` |
| Thay đổi so với phiên bản trước | UI/API/CSDL/ảnh/test/docs và lý do |
| Test tự động | Lệnh, hệ điều hành, kết quả |
| Kiểm thử thủ công | Ảnh, màn hình, chức năng được thử |
| Kiểm tra an toàn | Không có `.env`, `server/data/`, PII, credentials |
| PR và commit sau merge | Link PR, CI, SHA commit |
| Tag và release | Link GitHub Release **chỉ sau khi** merge + CI đạt |
| Rủi ro / quay lại bản trước | Backup `server/data/`, sơ đồ di trú, cách rollback |

## 8 bước bắt buộc

1. **Kiểm tra đầu vào:** tên và VERSION, cấu trúc thư mục, bảo mật khi giải nén; tính SHA-256, loại file rác `.venv`, `__pycache__`, DB, mật khẩu.
2. **Đối chiếu:** so với `main` và phiên bản trước; giữ `.github/`, `docs/`, `scripts/` dùng cho Git/CI; không xóa nhầm tài liệu/kiểm thử.
3. **Chuẩn hóa nhận diện:** LTD's Book Store, tên repo `LTDs-Book-Store`, đường dẫn/asset, không sửa nội dung bìa gốc.
4. **Kiểm tra nghiệp vụ:** giá, ảnh, tình trạng sách, banner, tài khoản, giỏ/đơn; tuyệt đối không tự đoán dữ liệu bán hàng.
5. **Kiểm thử:** Python/Node; thử trên Chromium desktop, mobile và Windows nếu khả dụng; lưu kết quả theo [evidence/README.md](evidence/README.md).
6. **Nhánh + PR:** thêm mã/ảnh/test/tài liệu trong nhánh riêng; chỉ merge khi CI Windows/Ubuntu đạt và kiểm tra diff.
7. **Phiên bản:** `VERSION`, CHANGELOG, README và tên ZIP cùng phiên bản; tạo tag từ commit đã được merge vào `main`, không tái sử dụng tag cũ.
8. **Bàn giao:** lưu biên bản kiểm thử, link Issue/PR/CI/Release và các giới hạn còn lại; **không triển khai VPS** khi chưa có yêu cầu.

## Cách tính SHA-256 trên Windows PowerShell

```powershell
Get-FileHash -Algorithm SHA256 .\LTDs-Book-Store-v0.9.0.zip
```

## Nguyên tắc dữ liệu & bảo mật

- Tuyệt đối không commit `.env`, token, file SQLite thật, `server/data/`, các bản backup hay tài liệu chứa thông tin khách hàng.
- Nếu ZIP chứa dữ liệu cá nhân: loại khỏi PR, không chép vào tài liệu minh chứng.
- Thử thay đổi schema trên DB giả lập, sao lưu trước khi nâng cấp bản local thực.
- Không đánh dấu kết quả kiểm thử từ ZIP là kết quả trên `main` khi chưa merge.
