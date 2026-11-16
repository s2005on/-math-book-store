# Checklist phát hành Math Book Store

**Áp dụng cho mỗi release; đây là checklist, không phải chứng nhận đã hoàn tất.**

- [ ] Mã nguồn của bản Windows cần phát hành đã được **đồng bộ đầy đủ** lên GitHub.
- [ ] VERSION, CHANGELOG, README và ghi chú release cùng một phiên bản.
- [ ] PR đã được rà soát `Files changed`; CI cả Ubuntu/Windows đều đạt.
- [ ] Các bài test backend, frontend và kiểm thử ZIP được chạy thành công.
- [ ] ZIP chứa file `RUN-WINDOWS.bat`, mã nguồn, ảnh sản phẩm đúng phiên bản và không có dữ liệu cá nhân.
- [ ] Ảnh bìa rõ, không méo; kiểm tra cả desktop và mobile.
- [ ] Thử tìm kiếm, giỏ, tài khoản, quản trị thêm/sửa/xóa và trạng thái sách.
- [ ] Nếu phiên bản có chức năng đơn hàng: kiểm tra giá phía server, quyền khách, đặt/hủy/xử lý đơn, dữ liệu không bị thất thoát.
- [ ] Có sao lưu `server/data/` trước khi nâng cấp dữ liệu local và hướng dẫn rollback.
- [ ] Gắn tag lên đúng commit trong `main`; ghi chú chức năng và giới hạn đã biết trong GitHub Release.
- [ ] Ghi bằng chứng test, ngày, môi trường và commit vào VERIFICATION.md hoặc file evidence phù hợp.

**Trạng thái 17/11/2026:** code GitHub đang là v0.5.1, ZIP local v0.6.0 **chưa đồng bộ**. Không tick các mục trên khi chưa có minh chứng. Xem [REPO-SYNC-STATUS.md](REPO-SYNC-STATUS.md).
