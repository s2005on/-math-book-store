# Quy ước phiên bản LTD's Book Store

Theo **SemVer** `MAJOR.MINOR.PATCH`: MAJOR khi thay đổi không tương thích; MINOR cho tính năng mới; PATCH cho sửa lỗi tương thích.

**Nguồn duy nhất:** file [VERSION](../VERSION) trong Git. `scripts/package.py` tự tạo ZIP `LTDs-Book-Store-v<version>.zip` theo nội dung này; `scripts/verify_package.py` xác nhận gói đầy đủ và không mang dữ liệu local.

## Điều kiện phát hành

1. PR đã merge lên `main`; CI Ubuntu/Windows đạt.
2. README, CHANGELOG và ghi chú phiên bản được cập nhật; phần chưa kiểm tra được liệt kê.
3. Kiểm thử giao diện liên quan, bảo vệ dữ liệu và chức năng chính.
4. Chủ dự án gắn tag `vX.Y.Z` vào đúng commit trên `main`.
5. Workflow [release.yml](../.github/workflows/release.yml) chỉ công bố ZIP nếu tag khớp VERSION **và** các bài test đạt.

Tag công bố không được di chuyển. Bản ZIP local v1.2.1 và mã nguồn GitHub v0.5.1 **chưa đồng bộ**; không tự động gắn tag v1.2.1 lên code cũ. Chỉ phát hành sau khi mã và ảnh đã được merge, kiểm thử trên đúng commit. Chi tiết: [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md).
