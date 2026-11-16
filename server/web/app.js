'use strict';

const $ = (id) => document.getElementById(id);
const money = (value) => new Intl.NumberFormat('vi-VN').format(value) + 'đ';
const normalize = (value) => String(value || '').toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
const escapeHTML = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

let products = [];
let activeCategory = 'Tất cả';
let cart = {};
let toastTimer = null;
const categories = ['Tất cả', 'Lớp 6', 'Lớp 7', 'Lớp 8', 'Lớp 9', 'Ôn thi lớp 10'];
const CART_KEY = 'math-book-store-cart-v020';

function loadCart() {
  try {
    const saved = JSON.parse(localStorage.getItem(CART_KEY) || '{}');
    if (!saved || typeof saved !== 'object' || Array.isArray(saved)) return;
    for (const [id, quantity] of Object.entries(saved)) {
      if (Number.isInteger(quantity) && quantity > 0 && quantity <= 99) cart[id] = quantity;
    }
  } catch { cart = {}; }
}

function persistCart() {
  try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch { /* Storage can be unavailable in private mode. */ }
  renderCart();
}

function showToast(message) {
  const toast = $('toast');
  toast.textContent = message;
  toast.classList.add('show');
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove('show'), 2300);
}

function renderCategories() {
  $('categoryTabs').replaceChildren(...categories.map((category) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `category-tab${category === activeCategory ? ' active' : ''}`;
    button.textContent = category;
    button.setAttribute('aria-pressed', String(category === activeCategory));
    button.addEventListener('click', () => {
      activeCategory = category;
      renderCategories();
      renderProducts();
    });
    return button;
  }));
}

function getVisibleProducts() {
  const query = normalize($('catalogSearch').value || $('searchInput').value);
  const sort = $('sortSelect').value;
  const found = products.filter((product) => {
    const categoryMatch = activeCategory === 'Tất cả' || product.category === activeCategory;
    const text = normalize(`${product.name} ${product.category} ${product.description} ${product.label}`);
    return categoryMatch && (!query || text.includes(query));
  });
  if (sort === 'price-asc') found.sort((a, b) => (a.price ?? Number.MAX_SAFE_INTEGER) - (b.price ?? Number.MAX_SAFE_INTEGER));
  else if (sort === 'price-desc') found.sort((a, b) => (b.price ?? -1) - (a.price ?? -1));
  else if (sort === 'name') found.sort((a, b) => a.name.localeCompare(b.name, 'vi'));
  else found.sort((a, b) => a.sortOrder - b.sortOrder);
  return found;
}

function productCard(product) {
  const price = product.price === null ? 'Liên hệ báo giá' : money(product.price);
  const priceClass = product.price === null ? ' contact-price' : '';
  const available = product.in_stock !== false && product.price !== null;
  const badgeClass = product.category === 'Ôn thi lớp 10' ? 'product-badge orange' : 'product-badge';
  const article = document.createElement('article');
  article.className = 'product-card';
  article.innerHTML = `
    <div class="product-visual">
      <span class="${badgeClass}">${escapeHTML(product.category)}</span>${product.in_stock === false ? '<span class="soldout">Hết hàng</span>' : ''}
      <img src="${escapeHTML(product.image)}" alt="${escapeHTML(product.name)}" loading="lazy" decoding="async" width="420" height="320">
    </div>
    <div class="product-body">
      <span class="product-kicker">${escapeHTML(product.label)}</span>
      <h3 class="product-title">${escapeHTML(product.name)}</h3>
      <p class="product-description">${escapeHTML(product.description)}</p>
      <div class="product-bottom"><strong class="product-price${priceClass}">${price}</strong><button class="detail-button" type="button" data-detail="${escapeHTML(product.id)}" aria-label="Xem chi tiết ${escapeHTML(product.name)}">↗</button></div>
      <button class="add-button" type="button" data-add="${escapeHTML(product.id)}" ${!available ? 'disabled' : ''}>${product.in_stock === false ? 'Hết hàng' : product.price === null ? 'Giá đang cập nhật' : '<span aria-hidden="true">＋</span> Thêm vào giỏ'}</button>
    </div>`;
  return article;
}

function renderProducts() {
  const found = getVisibleProducts();
  $('productGrid').replaceChildren(...found.map(productCard));
  $('resultCount').textContent = `${found.length} sản phẩm được tìm thấy`;
  $('emptyState').hidden = found.length > 0;
}

function addToCart(id) {
  const product = products.find((item) => item.id === id);
  if (!product || product.price === null || product.in_stock === false) return;
  cart[id] = Math.min(99, (cart[id] || 0) + 1);
  persistCart();
  showToast('Đã thêm sách vào giỏ hàng');
}

function cartQuantity() {
  return Object.values(cart).reduce((sum, quantity) => sum + quantity, 0);
}

function cartTotal() {
  return products.reduce((sum, product) => sum + (product.price || 0) * (cart[product.id] || 0), 0);
}

function renderCart() {
  for (const id of Object.keys(cart)) { const book=products.find(x=>x.id===id); if (!book || book.price===null || book.in_stock===false) delete cart[id]; }
  const count = cartQuantity();
  const total = money(cartTotal());
  $('cartCount').textContent = count;
  $('stickyCount').textContent = count;
  $('stickyTotal').textContent = total;
  $('cartTotal').textContent = total;
  $('checkoutTotal').textContent = total;
  $('stickyCart').hidden = count === 0;
  $('checkoutOpen').disabled = count === 0;

  const lines = products.filter((product) => cart[product.id] && product.price !== null && product.in_stock !== false);
  if (!lines.length) {
    $('cartLines').innerHTML = '<div class="cart-empty"><span>▤</span><b>Giỏ sách đang trống</b><small>Hãy chọn một vài cuốn sách bạn cần nhé.</small></div>';
    return;
  }
  $('cartLines').innerHTML = lines.map((product) => `
    <div class="cart-line">
      <img src="${escapeHTML(product.image)}" alt="" loading="lazy">
      <div><h3>${escapeHTML(product.name)}</h3><strong>${money(product.price)}</strong>
        <div class="quantity-control"><button type="button" data-quantity="minus" data-id="${escapeHTML(product.id)}" aria-label="Giảm số lượng">−</button><span>${cart[product.id]}</span><button type="button" data-quantity="plus" data-id="${escapeHTML(product.id)}" aria-label="Tăng số lượng">＋</button></div>
      </div>
      <button class="remove-line" type="button" data-quantity="remove" data-id="${escapeHTML(product.id)}" aria-label="Xóa ${escapeHTML(product.name)}">×</button>
    </div>`).join('');
}

function showProductDetails(id) {
  const product = products.find((item) => item.id === id);
  if (!product) return;
  const price = product.in_stock === false ? 'Hết hàng' : product.price === null ? 'Đang cập nhật' : money(product.price);
  $('productDialogContent').innerHTML = `
    <div class="product-detail-layout">
      <div class="product-detail-image"><img src="${escapeHTML(product.image)}" alt="${escapeHTML(product.name)}"></div>
      <div class="product-detail-copy">
        <div class="eyebrow"><span class="eyebrow-line"></span> ${escapeHTML(product.category.toUpperCase())}</div>
        <h2 id="productDialogTitle">${escapeHTML(product.name)}</h2>
        <p>${escapeHTML(product.description)}</p>
        <div class="detail-price">${price}</div>
        <div class="detail-meta">Ảnh bìa được xử lý từ hình ảnh sản phẩm do người bán cung cấp. Thông tin chi tiết sẽ được bổ sung khi có dữ liệu đầy đủ.</div>
        <button class="button button-primary" type="button" data-detail-add="${escapeHTML(product.id)}" ${product.price === null || product.in_stock === false ? 'disabled' : ''}>${product.in_stock === false ? 'Hết hàng' : product.price === null ? 'Chưa có giá bán' : 'Thêm vào giỏ hàng'} <span>→</span></button>
      </div>
    </div>`;
  $('productDialog').showModal();
}

function resetFilters() {
  activeCategory = 'Tất cả';
  $('catalogSearch').value = '';
  $('searchInput').value = '';
  $('sortSelect').value = 'featured';
  renderCategories();
  renderProducts();
}

async function init() {
  try {
    let response = await fetch('/api/books', { cache: 'no-store' }).catch(() => null);
    if (!response || !response.ok) response = await fetch('catalog.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Không tải được danh mục sách.');
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error('Dữ liệu danh mục không hợp lệ.');
    products = data.filter((item) => item && typeof item.id === 'string' && typeof item.name === 'string' && typeof item.image === 'string');
  } catch (error) {
    $('productGrid').innerHTML = '<div class="empty-state"><h3>Chưa thể tải danh mục sách</h3><p>Hãy chạy website thông qua máy chủ theo hướng dẫn trong README.</p></div>';
    $('resultCount').textContent = 'Lỗi tải dữ liệu';
    console.error(error);
    return;
  }

  try { const me=await fetch('/api/me').then(r=>r.json()); if (me.authenticated) { const link=$('accountLink');if(link){link.textContent=me.role==='admin'?'Quản trị':'Xin chào, '+me.username;link.href=me.role==='admin'?'/admin.html':'/account.html';} } } catch {}
  loadCart();
  renderCategories();
  renderProducts();
  renderCart();

  $('categoryTabs').addEventListener('keydown', (event) => {
    if (event.key === 'Escape') $('catalogSearch').focus();
  });
  $('productGrid').addEventListener('click', (event) => {
    const addButton = event.target.closest('[data-add]');
    const detailButton = event.target.closest('[data-detail]');
    if (addButton) addToCart(addButton.dataset.add);
    if (detailButton) showProductDetails(detailButton.dataset.detail);
  });
  $('productDialogContent').addEventListener('click', (event) => {
    const button = event.target.closest('[data-detail-add]');
    if (!button) return;
    addToCart(button.dataset.detailAdd);
    $('productDialog').close();
  });
  $('cartLines').addEventListener('click', (event) => {
    const button = event.target.closest('[data-quantity]');
    if (!button) return;
    const { id, quantity: action } = button.dataset;
    if (action === 'remove') delete cart[id];
    else if (action === 'plus') cart[id] = Math.min(99, (cart[id] || 0) + 1);
    else if (action === 'minus') {
      cart[id] = (cart[id] || 0) - 1;
      if (cart[id] <= 0) delete cart[id];
    }
    persistCart();
  });

  $('searchInput').addEventListener('input', () => { $('catalogSearch').value = $('searchInput').value; renderProducts(); });
  document.addEventListener('keydown', (event) => {
    const target = event.target;
    const editing = target && (target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName));
    if (event.key === '/' && !editing) { event.preventDefault(); $('searchInput').focus(); }
  });
  $('catalogSearch').addEventListener('input', () => { $('searchInput').value = $('catalogSearch').value; renderProducts(); });
  $('sortSelect').addEventListener('change', renderProducts);
  $('clearFilters').addEventListener('click', (event) => { event.preventDefault(); resetFilters(); });
  $('resetSearch').addEventListener('click', resetFilters);
  $('cartOpen').addEventListener('click', () => $('cartDialog').showModal());
  $('stickyCartOpen').addEventListener('click', () => $('cartDialog').showModal());
  $('cartClose').addEventListener('click', () => $('cartDialog').close());
  $('cartDialog').addEventListener('click', (event) => { if (event.target === $('cartDialog')) $('cartDialog').close(); });
  $('productDialogClose').addEventListener('click', () => $('productDialog').close());
  $('productDialog').addEventListener('click', (event) => { if (event.target === $('productDialog')) $('productDialog').close(); });
  $('checkoutClose').addEventListener('click', () => $('checkoutDialog').close());
  $('checkoutOpen').addEventListener('click', () => {
    if (!cartQuantity()) return;
    $('cartDialog').close();
    $('checkoutTotal').textContent = money(cartTotal());
    $('checkoutDialog').showModal();
  });
  $('checkoutForm').addEventListener('submit', (event) => {
    event.preventDefault();
    if (!cartQuantity()) return;
    const orderCode = `MBS-${new Date().toISOString().slice(2,10).replaceAll('-', '')}-${Math.floor(1000 + Math.random() * 9000)}`;
    cart = {};
    persistCart();
    event.currentTarget.reset();
    $('checkoutDialog').close();
    showToast(`Đã tạo đơn demo ${orderCode}. Chưa gửi đến người bán.`);
  });
  $('mobileMenu').addEventListener('click', () => {
    const isOpen = $('mobileMenu').getAttribute('aria-expanded') === 'true';
    $('mobileMenu').setAttribute('aria-expanded', String(!isOpen));
    $('mobileNav').hidden = isOpen;
  });
  $('mobileNav').addEventListener('click', (event) => {
    if (event.target.closest('a')) { $('mobileNav').hidden = true; $('mobileMenu').setAttribute('aria-expanded', 'false'); }
  });
}

init();