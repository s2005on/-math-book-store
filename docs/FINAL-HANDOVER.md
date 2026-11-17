# Bàn giao LTD's Book Store — sổ theo dõi phiên bản

## 1. Hồ sơ Sprint 0 (lịch sử)

Giai đoạn UI Foundation từng bàn giao giao diện danh mục, giỏ demo, mã FastAPI nền, tài liệu WBS/Scrum và CI. Những kết quả đó thuộc **phiên bản/commit của Sprint 0**, không đại diện cho chức năng mới ở `main` và **không phải** kết quả test ZIP local v1.2.1.

## 2. Cơ sở ở GitHub hiện tại

- Repository: https://github.com/s2005on/LTDs-Book-Store
- `VERSION` trên `main`: **v0.5.1** (cho đến khi PR đồng bộ mới được merge).
- Nghiệp vụ mã nguồn hiện có: FastAPI/SQLite, đăng nhập/đăng ký, quản trị sách, upload ảnh, trạng thái sách, cửa hàng, giỏ demo.
- Chưa đồng bộ: order API/quản trị đơn và bộ ảnh gốc chất lượng cao từ ZIP local v1.2.1.
- Chưa triển khai VPS; không đưa `.env`, SQLite khách, backup hoặc PII vào GitHub.

## 3. Hồ sơ và quy trình đi kèm

| Thành phần | Tài liệu |
|---|---|
| Phân tích/thiết kế | [ACADEMIC-TRACEABILITY.md](ACADEMIC-TRACEABILITY.md), [03-system-design.md](03-system-design.md) |
| Sprint/tiến độ | [SPRINT-TRACKER.md](SPRINT-TRACKER.md) |
| Chất lượng/test | [TEST-PLAN.md](TEST-PLAN.md), [QUALITY.md](QUALITY.md) |
| Minh chứng | [evidence/README.md](evidence/README.md) |
| Nhận bản ZIP mới | [VERSION-INTAKE.md](VERSION-INTAKE.md) |
| Release/rollback | [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md), [VERSIONING.md](VERSIONING.md) |

## 4. Checklist bàn giao mỗi phiên bản

- [ ] Có ZIP chính thức, SHA-256 và VERSION đúng.
- [ ] Nhánh PR chứa code, ảnh và test đầy đủ.
- [ ] CI Windows/Ubuntu đạt **trên đúng SHA**.
- [ ] Minh chứng UI và API được lưu thực tế theo commit.
- [ ] Backup dữ liệu local và thử nâng cấp/khôi phục nếu có thay đổi DB.
- [ ] README, CHANGELOG, tag và GitHub Release nhất quán.
- [ ] Có ghi rõ các lỗi còn lại và giới hạn; không tuyên bố chạy VPS khi chưa kiểm thử.

## 5. Trạng thái hiện tại và bước tiếp theo

**Chưa coi là bàn giao v1.2.1 trên GitHub** vì mã ZIP chưa nhập vào `main`. Theo dõi [Issue #3](https://github.com/s2005on/LTDs-Book-Store/issues/10). Khi người dùng gửi bản mới, đối chiếu theo [VERSION-INTAKE.md](VERSION-INTAKE.md), PR → CI → merge → release, rồi mới cập nhật kết luận hồ sơ này.
