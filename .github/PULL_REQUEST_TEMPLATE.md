## Mục tiêu & Issue liên quan

- Issue:
- Nội dung thay đổi (không ghi chung chung):

## Phạm vi

- [ ] Giao diện khách / responsive / ảnh sản phẩm
- [ ] Sản phẩm, giá, tồn kho, sắp ra mắt
- [ ] Tài khoản / quyền truy cập
- [ ] Đơn hàng / CSDL / backup
- [ ] Test / CI / đóng gói ZIP
- [ ] Tài liệu / release

## Kiểm thử và bằng chứng

- [ ] `python -m unittest discover -s tests -v`
- [ ] `node --check server/web/app.js` và `node --test tests/*.test.cjs`
- [ ] `python scripts/package.py` và `python scripts/verify_package.py` (nếu thay đổi packaging)
- [ ] Desktop/mobile: ảnh hoặc ghi chú bước thực hiện (nếu thay đổi UI)
- [ ] GitHub CI Ubuntu + Windows đạt

## Rủi ro và trạng thái đồng bộ

- Dữ liệu/cấu hình: không commit `.env`, `server/data/`, bí mật hoặc dữ liệu khách.
- Phiên bản của source GitHub và bản ZIP local có khớp không?
- Việc chưa test / chưa làm:
- Có cần migration / sao lưu `server/data/` trước nâng cấp không?
