# 03 — Thiết kế hệ thống

## Kiến trúc hiện tại

```text
Browser
  ├── server/web/index.html
  ├── server/web/styles.css
  ├── server/web/app.js
  ├── server/web/catalog.json
  └── server/web/assets/books/*
          │
          ▼
FastAPI static host (server/app.py)
  └── GET /health
```

FastAPI hiện chỉ phục vụ file tĩnh và endpoint health. Chưa có API nghiệp vụ hay database.

## Thành phần giao diện

- `index.html`: storefront, hero, danh mục, card, dialog và footer.
- `app.js`: tải catalog, lọc/tìm kiếm/sắp xếp, cart, chi tiết và checkout demo.
- `styles.css`: design tokens, layout, responsive, sticky header và sticky cart.
- `catalog.json`: dữ liệu mẫu độc lập với giao diện.
- `admin.html` / `admin.css`: bản xem trước bố cục quản trị tĩnh.

## Dữ liệu sản phẩm

Mỗi sản phẩm có `id`, `name`, `category`, `price`, `image`, `description`, `label` và `sortOrder`. `price: null` thể hiện chưa có giá được xác nhận; sản phẩm này không thể thêm vào giỏ.

## Thiết kế ảnh bìa

Ảnh bìa được cắt phối cảnh từ ảnh gốc, dựng thành mockup có bóng đổ và nền trong suốt/neutral. Không tái tạo chữ bằng mô hình sinh ảnh để tránh sai tên sách hoặc nội dung bìa. Ảnh gốc không đưa vào repository công khai; chỉ lưu ảnh đã xử lý.

## Kiến trúc mục tiêu

```text
Browser ── HTTPS ──> Nginx ──> FastAPI
                                  ├── Catalog API
                                  ├── Cart / Order API
                                  ├── Admin Auth + Admin API
                                  └── SQLite (MVP) / PostgreSQL (scale)
```

Schema dự kiến: `admins`, `products`, `orders`, `order_items`, `order_events`, `settings`. Thiết kế schema chi tiết cần được chốt trước Sprint 1.

## Rủi ro và quyết định

- Giá sản phẩm có thể thay đổi: backend cần tính giá tại thời điểm checkout.
- Thông tin sách còn thiếu: không tự suy đoán; đánh dấu cần cập nhật.
- Ảnh chụp có phối cảnh: xử lý hình học để giữ nguyên nội dung bìa.
- Frontend-only không đủ để vận hành bán hàng: giữ thông báo rõ ràng ở checkout.
