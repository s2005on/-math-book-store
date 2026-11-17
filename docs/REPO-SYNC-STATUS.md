# Trạng thái đồng bộ mã nguồn và các bản ZIP

**Ngày rà soát:** 18/11/2026. Mục tiêu của bảng này là giúp người xem GitHub phân biệt **mã thực có trên `main`** với những bản website đã được đóng gói và thử nghiệm riêng trên máy.

| Thành phần | Repository `main` | ZIP local mới nhất |
|---|---|---|
| Phiên bản | `0.5.1` | `1.2.1` — Auth Update |
| Mã backend | FastAPI + SQLite, đăng nhập, CRUD sách | Có các tính năng bổ sung của Art Edition |
| Giao diện khách | Danh mục, lọc, chi tiết và giỏ demo | Có phần nâng cấp giao diện; trang đăng nhập và đăng ký riêng |
| Đăng ký | Tên đăng nhập và mật khẩu | Thêm họ tên và **số điện thoại bắt buộc** |
| Đơn hàng | Chưa có backend lưu/xử lý đơn hoàn chỉnh | Có trong mã ZIP local, chưa nhập GitHub |
| Ảnh sách | Chủ yếu asset minh họa nhỏ | Có ảnh WebP độ phân giải cao và ảnh gốc |
| Theme, khuyến mãi, nội dung | Chưa đủ các chức năng Art Edition | Có thay đổi trong bản ZIP |
| Kiểm thử CI | Có CI Ubuntu + Windows cho commit của `main` | **Chưa có CI của GitHub trên mã v1.2.1** |
| VPS / thanh toán thật | Chưa triển khai | Chưa triển khai |

**Không dùng kết quả test ZIP local để tuyên bố các chức năng đã có hoặc đã được kiểm thử trên `main`.**

## Mốc và hồ sơ

- **v0.5.1**: phiên bản mã nguồn đang nằm trên GitHub.
- **v1.2.0 Art Edition**: [biên bản tiếp nhận](RELEASE-INTAKE-v1.2.0.md); hiện là mốc lịch sử.
- **v1.2.1 Auth Update**: [biên bản tiếp nhận mới nhất](RELEASE-INTAKE-v1.2.1.md), có SHA-256 ZIP, tên file và checklist.
- [Issue #10](https://github.com/s2005on/LTDs-Book-Store/issues/10): công việc đưa app, kiểm thử và ảnh mới lên repository.
- [VERSION-INTAKE.md](VERSION-INTAKE.md): quy trình nhận các ZIP sắp tới.

## Checklist để chuyển v1.2.1 lên `main`

- [ ] Tạo nhánh import từ `main`, đối chiếu code ZIP với phiên bản GitHub.
- [ ] Giữ nguyên `.github/`, `docs/`, `scripts/` và lịch sử Git.
- [ ] Nhập đầy đủ ảnh, backend, frontend, tests và migration tài khoản.
- [ ] Không upload `.env`, `.venv`, `server/data/`, SQLite chứa người dùng/đơn hàng.
- [ ] Kiểm thử đăng ký yêu cầu điện thoại và bảo đảm tài khoản cũ vẫn hoạt động.
- [ ] Chạy CI Windows/Ubuntu, test giao diện desktop/mobile và ghi minh chứng đúng commit.
- [ ] Review PR, merge vào `main`, đồng bộ VERSION và CHANGELOG.
- [ ] Kiểm tra CI `main` rồi mới tạo GitHub Release/tag `v1.2.1`.

**Lưu ý:** repo được tổ chức và chuẩn hóa tài liệu từ bây giờ không đồng nghĩa chức năng v1.2.1 đã được merge. Đợt làm việc này chỉ chỉnh **trình bày GitHub và quy trình**, không sửa code website và không động vào VPS.
