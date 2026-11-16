# Quy ước phiên bản LTD's Book Store

Theo **SemVer** `MAJOR.MINOR.PATCH`: MAJOR khi thay đổi không tương thích; MINOR cho tính năng mới; PATCH cho sửa lỗi tương thích.

**Nguồn duy nhất:** file [VERSION](../VERSION) trong Git. `scripts/package.py` tự tạo ZIP `LTDs-Book-Store-v<version>.zip` theo nội dung này; `scripts/verify_package.py` xác nhận gói đầy đủ và không mang dữ liệu local.

## Điều kiện phát hành

1. PR đã merge lên `main`; CI Ubuntu/Windows đạt.
2. README, CHANGELOG và ghi chú phiên bản được cập nhật; phần chưa kiểm tra được liệt kê.
3. Kiểm thử giao diện liên quan, bảo vệ dữ liệu và chức năng chính.
4. Chủ dự án gắn tag `vX.Y.Z` vào đúng commit trên `main`.
5. Workflow [release.yml](../.github/workflows/release.yml) chỉ công bố ZIP nếu tag khớp VERSION **và** các bài test đạt.

Tag công bố không được di chuyển. Bản ZIP v0.9.0 trên máy và mã nguồn GitHub v0.5.1 **chưa đồng bộ**, không tự động phát hành v0.6.0 từ mã cũ. Chi tiết: [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md).
