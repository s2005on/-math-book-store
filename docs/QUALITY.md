# Quản lý chất lượng — LTD's Book Store

## Mục tiêu

1. Mã nguồn nhất quán với ảnh/tài liệu/giá bán, UI responsive và ảnh bìa rõ, **không tự thay bìa gốc**.
2. Tính năng quan trọng có test thích hợp, API xác thực và phân quyền từ máy chủ; không tin giá do browser gửi.
3. `main` chỉ nhận thay đổi qua PR có CI xanh và người thực hiện đã xem diff.
4. ZIP phát hành đúng phiên bản, có thể khởi động trên Windows, không chứa bí mật hay dữ liệu khách thật.
5. Trạng thái hoàn thành và minh chứng kiểm thử là **thật**, đúng commit; không tính kế hoạch như đã thực hiện.

## Điều kiện Done

- Có liên kết issue/user story (khi phù hợp), mô tả thay đổi và tiêu chí nghiệm thu.
- Code/docs/asset nhất quán; không đưa `.env`, DB, `server/data/`, token, PII vào Git.
- Unit/API/Node test liên quan đạt, CI Ubuntu/Windows xanh.
- Với UI: kiểm tra desktop/mobile và lưu ảnh của đúng phiên bản; khi chưa kiểm thử phải ghi `chưa xác minh`.
- Với CSDL: lưu ý migration, backup và rollback.
- Với release: `VERSION`, `CHANGELOG.md`, ZIP và tag phải khớp.
- PR được rà soát; tự kiểm thử **không thay thế** review độc lập của giảng viên/người khác.

## Tài liệu và kiểm chứng

- [TEST-PLAN.md](TEST-PLAN.md): tình huống kiểm thử cần làm.
- [ACADEMIC-TRACEABILITY.md](ACADEMIC-TRACEABILITY.md): yêu cầu ↔ minh chứng ↔ mã nguồn.
- [evidence/README.md](evidence/README.md): tiêu chuẩn lưu ảnh/log.
- [VERSION-INTAKE.md](VERSION-INTAKE.md): cách kiểm soát ZIP mới do chủ dự án gửi.
- [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md): kiểm soát bản phát hành.
