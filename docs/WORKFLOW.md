# Quy trình phát triển LTD's Book Store

Áp dụng cho đồ án cuối kỳ, ưu tiên **bản chạy Windows** và dữ liệu an toàn. Quy trình riêng của LTD's Book Store gồm Scrum rút gọn, Git/PR, CI hai hệ điều hành, SemVer, changelog và lưu minh chứng kiểm thử.

## 1. Chu trình một sprint

- Chu kỳ đề xuất: **1 tuần**; backlog trong GitHub Issues, trạng thái **To do / Doing / Done**.
- Đầu sprint: chọn mục tiêu cụ thể (ví dụ sửa đăng nhập, quản lý đơn, ảnh rõ nét).
- Trong sprint: mỗi thay đổi đi trên nhánh riêng; cập nhật issue và kiểm thử.
- Cuối sprint: demo ứng dụng chạy local, ghi nhận lỗi, quyết định chuyển sang sprint tiếp theo.

Do đồ án cá nhân, Product Owner, điều phối, lập trình và kiểm thử có thể kiêm nhiệm. Tự kiểm tra **không phải** xác nhận đã được giảng viên/người khác review.

## 2. Git và Pull Request

1. `main` là nhánh chuẩn của **mã nguồn trong GitHub**, hạn chế sửa trực tiếp.
2. Tạo nhánh `feat/`, `fix/`, `docs/`, `test/`, `chore/`.
3. Commit theo mẫu `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
4. Một PR cho một nhóm thay đổi rõ ràng, liên kết issue nếu có; ghi rủi ro, kiểm thử và ảnh chụp liên quan.
5. Trước merge: xem `Files changed`, chạy CI **Ubuntu + Windows** và soát quyền truy cập/mật khẩu.
6. Chỉ merge khi kiểm thử đạt; nếu chưa thể tự động kiểm tra bằng trình duyệt thì ghi riêng phần **chưa kiểm tra trực quan**.

Không force-push `main`, không đưa `.env`, `server/data/`, thông tin khách hàng, ảnh cá nhân hoặc bản sao lưu lên Git.

## 3. Chất lượng và bằng chứng

Kiểm thử được tự động hóa (theo khả năng của phiên bản mã nguồn):
- Python: `python -m unittest discover -s tests -v`.
- JavaScript: `node --check server/web/app.js`, `node --test tests/*.test.cjs`.
- Đóng gói: `python scripts/package.py`, `python scripts/verify_package.py`.
- CI trên GitHub Actions kiểm tra Ubuntu/Windows, tải ZIP chỉ sau khi toàn bộ bước liên quan đạt.

Kiểm thử thủ công trước demo: màn hình desktop + điện thoại; tìm kiếm/lọc; mở chi tiết sách; thêm giỏ; đăng nhập; quyền quản trị; thêm/sửa/xóa sách; trạng thái còn hàng/hết hàng/sắp ra mắt; ảnh bìa nét; **đặt đơn/lịch sử đơn** chỉ khi mã nguồn được đồng bộ và chức năng đó thật sự có trên nhánh.

Khi lưu bằng chứng: ghi ngày, commit/tag, hệ điều hành, bước thực hiện, kết quả mong đợi và kết quả thực tế. Nếu lỗi được tìm thấy, mở issue, sửa và chạy lại; không đánh dấu đạt bằng suy đoán.

## 4. Phiên bản và release

- `VERSION` là nguồn duy nhất xác định tên gói `LTDs-Book-Store-vX.Y.Z.zip`.
- Với tính năng mới dùng tăng **MINOR**; sửa lỗi tương thích tăng **PATCH**; thay đổi không tương thích tăng **MAJOR**.
- Cập nhật `CHANGELOG.md` và ghi chú release, chạy CI trên nhánh trước.
- Sau khi PR được merge và xác nhận `main` xanh, gắn tag `vX.Y.Z` vào đúng commit trên `main`. Workflow `release.yml` chạy lại kiểm thử, kiểm tra tên tag khớp VERSION, đóng gói ZIP và xuất bản GitHub Release.
- Không gắn/di chuyển tag đã công bố và không dùng số phiên bản của ZIP local để khẳng định mã nguồn GitHub đã đồng bộ.

## 5. Quy tắc dữ liệu và phạm vi

- Chạy local, **chưa triển khai VPS** theo ưu tiên hiện tại.
- Sao lưu `server/data/` trước khi đổi phiên bản; bảo vệ `.env` và mật khẩu admin.
- Chỉ dùng ảnh bìa do chủ dự án cung cấp hoặc có quyền sử dụng. Ưu tiên WebP chất lượng đủ hiển thị; không thay đổi thiết kế bìa.
- Trước khi sử dụng thực tế phải kiểm tra bảo mật, lỗi mạng, bảo vệ dữ liệu khách và các luồng tiền/đơn; hiện mặc định là **đồ án demo nội bộ**.

## 6. Trạng thái đồng bộ

Xem [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md), [RELEASE-INTAKE-v1.2.1.md](RELEASE-INTAKE-v1.2.1.md), [VERSION-INTAKE.md](VERSION-INTAKE.md) và [ACADEMIC-TRACEABILITY.md](ACADEMIC-TRACEABILITY.md). **Bản ZIP v1.2.1 đang dùng trên máy chưa đồng nghĩa với mã nguồn `main` hiện tại (v0.5.1)**. Cần đối chiếu, nhập và kiểm thử trước khi phát hành phiên bản v1.2.1 từ GitHub.

## 7. Bàn giao học phần và các bản ZIP tiếp theo

- Chỉ tiếp nhận phiên bản theo [VERSION-INTAKE.md](VERSION-INTAKE.md): SHA-256 ZIP, diff, kiểm tra secrets, test, PR, tag.
- Lưu bằng chứng thật đúng commit trong [docs/evidence](evidence/README.md) (UI desktop/mobile, test backend/frontend, CI).
- Mỗi Sprint có mục tiêu, issue/PR và kết quả demo ở [SPRINT-TRACKER.md](SPRINT-TRACKER.md).
- Không tăng VERSION hoặc tạo tag thay người dùng khi chưa nhận và kiểm chứng bản cập nhật. Không nói các phiên bản ZIP local đã lên `main` khi chưa merge.
