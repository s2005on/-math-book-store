# Pull Request Review Checklist

- Scope is clear and related to one issue/backlog item.
- No secrets, local database, customer data or raw source images are committed.
- Catalog schema and product image references remain valid.
- UI changes are responsive and keyboard-accessible.
- Python and Node tests pass.
- Demo-only behavior is clearly labeled.
- Documentation and CHANGELOG are updated where needed.
- Production claims are not made for unimplemented API or payment features.

## Kiểm tra riêng cho đồ án học thuật

- [ ] Có liên hệ Issue/User Story/Sprint ở [SPRINT-TRACKER.md](SPRINT-TRACKER.md) hoặc [ACADEMIC-TRACEABILITY.md](ACADEMIC-TRACEABILITY.md).
- [ ] Với UI, lưu ảnh desktop/mobile của **đúng commit**; nếu chưa kiểm tra, ghi rõ.
- [ ] Với bản ZIP mới, kiểm tra [VERSION-INTAKE.md](VERSION-INTAKE.md), SHA-256, ảnh bìa nét và trạng thái có thể mua.
- [ ] Không dùng test từ ZIP local làm bằng chứng CI của `main` trước khi nhập mã.
- [ ] Không tạo tag/release trước khi VERSION, CHANGELOG, ZIP và CI khớp nhau.
