# Bắt đầu chạy Math Book Store

## Windows
1. Cài Python 3.11+.
2. Chạy `RUN-WINDOWS.bat`.
3. Truy cập http://127.0.0.1:8017/
4. Admin UI preview: http://127.0.0.1:8017/admin.html
5. Health: http://127.0.0.1:8017/health

## macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r server/requirements.txt
python -m uvicorn server.app:app --host 127.0.0.1 --port 8017
```

## Kiểm thử
```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -v
node --test tests/*.test.cjs
```

Giỏ hàng demo chỉ lưu ở trình duyệt hiện tại. Checkout không gửi đơn hàng. Không nhập thông tin cá nhân thật.