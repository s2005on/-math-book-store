# Tiếp nhận LTD's Book Store v1.2.1 — Auth Update

**Ngày đối chiếu:** 18/11/2026. **Phạm vi:** hồ sơ nhận ZIP do chủ dự án cung cấp, **chưa phải GitHub Release**.

## 1. Thông tin tệp đầu vào

| Trường | Giá trị |
|---|---|
| Tên gói | `LTDs-Book-Store-v1.2.1-Auth-Update.zip` |
| Phiên bản bên trong | `VERSION=1.2.1` |
| Kích thước | 19.840.431 byte (khoảng 19,8 MB) |
| Số mục ZIP | 61 |
| SHA-256 | `25e5b884eee7d457f43e2a62312023457e3666c9d80171170f21c545d984b95f` |
| Kiểm tra ZIP | CRC hợp lệ; có `server/app.py`, `login.html`, `register.html` |
| Trạng thái GitHub `main` | `0.5.1` — chưa nhập nội dung ZIP |

> SHA-256 dùng xác định đúng tệp ZIP đã được kiểm tra trong phiên làm việc, không chứng nhận các tính năng đã chạy trên GitHub.

## 2. Khác biệt đáng chú ý

- Giao diện đăng nhập và đăng ký là **hai trang riêng**.
- Đăng ký có họ tên, tên đăng nhập, số điện thoại bắt buộc, mật khẩu và xác nhận mật khẩu.
- Backend có mã xử lý `phone` và `full_name`. Thay đổi cấu trúc lưu tài khoản cần kiểm thử migration với SQLite đã có dữ liệu.
- Không có nút đăng nhập Google, Facebook hoặc Apple trong hai trang xác thực.
- Những thay đổi thuộc **bản ZIP local**, không được trình bày như thể đã có trên `main`.

## 3. Việc cần thực hiện trước khi cập nhật GitHub Release

- [x] Kiểm tra định dạng ZIP và SHA-256 của tệp đầu vào.
- [x] Kiểm tra VERSION và sự tồn tại của hai trang xác thực.
- [ ] So sánh source và ảnh sản phẩm với `main`, không làm mất dữ liệu trong các thư mục `docs/`, `.github/`, `scripts/`.
- [ ] Đưa mã nguồn, ảnh, tài liệu và kiểm thử tương ứng lên **nhánh riêng** (không đẩy dữ liệu runtime).
- [ ] Kiểm tra số điện thoại sai/đúng, đăng nhập cũ, đăng ký mới, phân quyền và nâng cấp database.
- [ ] Chạy CI Python/Node trên Windows và Ubuntu của đúng PR.
- [ ] Review diff, kiểm tra UI desktop/mobile thật, lưu minh chứng vào [evidence](evidence/README.md).
- [ ] Merge khi đạt, đồng bộ VERSION/CHANGELOG và chạy CI trên `main`.
- [ ] Sau đó mới tạo tag và GitHub Release đúng phiên bản.

## 4. Lưu ý bảo mật

Không commit `.env`, `.venv/`, `server/data/`, database SQLite, dữ liệu khách, token hoặc mật khẩu. File cấu hình mẫu `.env.example` không phải bí mật. Sao lưu dữ liệu trên máy trước khi cập nhật.

**Bản trước:** [Biên bản tiếp nhận Art Edition v1.2.0](RELEASE-INTAKE-v1.2.0.md).  
**Công việc đồng bộ:** [Issue #10](https://github.com/s2005on/LTDs-Book-Store/issues/10).  
**Quy trình:** [VERSION-INTAKE.md](VERSION-INTAKE.md).
