'use strict';

const $ = (id) => document.getElementById(id);
const money = (value) => new Intl.NumberFormat('vi-VN').format(value) + 'đ';
const normalize = (value) => String(value || '').toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
const escapeHTML = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));

let products = [];
let categories = ['Tất cả', 'Lớp 6', 'Lớp 7', 'Lớp 8', 'Lớp 9', 'Ôn thi lớp 10'];
let activeCategory = 'Tất cả';
let activeGoal = 'all';
let activePriceRange = 'all';
let inStockOnly = false;
let wishlistOnly = false;
let activePromo = '';
let activePromoDiscount = 0;
let promosEnabled = false;
let shippingEnabled = false;
let freeshipThreshold = 200000;
let baseShippingFee = 25000;
let currentUser = null;
let lastOrderReceipt = null;
let cart = {};
let wishlist = new Set();
let recentIds = [];
let toastTimer = null;

const CART_KEY = 'ltds-book-store-cart-v120';
const WISHLIST_KEY = 'ltds-book-store-wishlist-v120';
const RECENT_KEY = 'ltds-book-store-recent-v130';
const LEGACY_CART_KEY = 'math-book-store-cart-v060';
const LEGACY_WISHLIST_KEY = 'math-book-store-wishlist-v080';

const stockQtyOf = (p) => (typeof p.stock_qty === 'number' ? p.stock_qty : (p.in_stock === false || p.status !== 'available' ? 0 : 50));
const isAvailable = (p) => (p.status ? p.status === 'available' : p.in_stock !== false) && p.price !== null && stockQtyOf(p) > 0;
const statusText = (p) => p.status === 'coming_soon' ? 'Sắp ra mắt' : (!isAvailable(p) && p.price !== null ? 'Hết hàng' : '');

function loadCart() {
  try {
    const saved = JSON.parse(localStorage.getItem(CART_KEY) || localStorage.getItem(LEGACY_CART_KEY) || '{}');
    if (!saved || typeof saved !== 'object' || Array.isArray(saved)) return;
    for (const [id, quantity] of Object.entries(saved)) {
      if (Number.isInteger(quantity) && quantity > 0 && quantity <= 99) cart[id] = quantity;
    }
  } catch { cart = {}; }
}

function loadWishlist() {
  try {
    const saved = JSON.parse(localStorage.getItem(WISHLIST_KEY) || localStorage.getItem(LEGACY_WISHLIST_KEY) || '[]');
    if (Array.isArray(saved)) wishlist = new Set(saved.filter(x => typeof x === 'string'));
  } catch { wishlist = new Set(); }
}

function loadRecent() {
  try {
    const saved = JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
    if (Array.isArray(saved)) recentIds = saved.filter(x => typeof x === 'string').slice(0, 6);
  } catch { recentIds = []; }
}

function pushRecent(id) {
  recentIds = [id, ...recentIds.filter(x => x !== id)].slice(0, 6);
  try { localStorage.setItem(RECENT_KEY, JSON.stringify(recentIds)); } catch {}
  renderRecentlyViewed();
}

function persistWishlist() {
  try { localStorage.setItem(WISHLIST_KEY, JSON.stringify([...wishlist])); } catch {}
  const cnt = $('wishlistCount');
  if (cnt) cnt.textContent = wishlist.size;
}

function persistCart() {
  try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch {}
  renderCart();
}

function showToast(message) {
  const toast = $('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove('show'), 2600);
}

function calcShipping(subtotal) {
  if (!shippingEnabled || subtotal <= 0) return 0;
  if (freeshipThreshold > 0 && subtotal >= freeshipThreshold) return 0;
  return baseShippingFee;
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

function matchesGoal(product) {
  if (activeGoal === 'all') return true;
  const hay = normalize(`${product.id} ${product.name} ${product.label} ${product.category}`);
  if (activeGoal === 'hsg') return hay.includes('hsg') || hay.includes('hoc sinh gioi');
  if (activeGoal === 'exam10') return hay.includes('lop 10') || hay.includes('63 de') || hay.includes('luyen thi');
  if (activeGoal === 'foundation') return hay.includes('bai tap thuc hanh') || hay.includes('co ban');
  return true;
}

function matchesPrice(product) {
  if (activePriceRange === 'all') return true;
  if (product.price === null) return false;
  if (activePriceRange === 'under100') return product.price < 100000;
  if (activePriceRange === '100to200') return product.price >= 100000 && product.price <= 200000;
  if (activePriceRange === 'over200') return product.price > 200000;
  return true;
}

function getVisibleProducts() {
  const query = normalize($('searchInput').value || ($('catalogSearch') ? $('catalogSearch').value : ''));
  const sort = $('sortSelect').value;
  const found = products.filter((product) => {
    if (product.status === 'coming_soon') return false;
    const categoryMatch = activeCategory === 'Tất cả' || product.category === activeCategory;
    const goalMatch = matchesGoal(product);
    const priceMatch = matchesPrice(product);
    const stockMatch = !inStockOnly || isAvailable(product);
    const favMatch = !wishlistOnly || wishlist.has(product.id);
    const text = normalize(`${product.name} ${product.category} ${product.description} ${product.label}`);
    return categoryMatch && goalMatch && priceMatch && stockMatch && favMatch && (!query || text.includes(query));
  });
  if (sort === 'price-asc') found.sort((a, b) => (a.price ?? Number.MAX_SAFE_INTEGER) - (b.price ?? Number.MAX_SAFE_INTEGER));
  else if (sort === 'price-desc') found.sort((a, b) => (b.price ?? -1) - (a.price ?? -1));
  else if (sort === 'rating-desc') found.sort((a, b) => (b.rating_avg || 0) - (a.rating_avg || 0) || (b.review_count || 0) - (a.review_count || 0));
  else if (sort === 'name') found.sort((a, b) => a.name.localeCompare(b.name, 'vi'));
  else found.sort((a, b) => (a.sortOrder ?? 100) - (b.sortOrder ?? 100));
  return found;
}

function productCard(product) {
  const price = product.price === null ? 'Liên hệ báo giá' : money(product.price);
  const priceClass = product.price === null ? ' contact-price' : '';
  const available = isAvailable(product);
  const qty = stockQtyOf(product);
  const badgeClass = product.category === 'Ôn thi lớp 10' ? 'product-badge orange' : 'product-badge';
  const isFav = wishlist.has(product.id);
  const ratingHtml = product.review_count > 0
    ? `<span class="card-rating" title="${product.review_count} đánh giá">★ ${Number(product.rating_avg).toFixed(1)} <small>(${product.review_count})</small></span>`
    : '';
  const stockTag = !available
    ? (statusText(product) ? `<span class="soldout">${escapeHTML(statusText(product))}</span>` : '')
    : (qty <= 5 ? `<span class="lowstock-pill">Chỉ còn ${qty} cuốn</span>` : '');

  const article = document.createElement('article');
  article.className = 'product-card';
  article.innerHTML = `
    <div class="product-visual" data-detail="${escapeHTML(product.id)}" role="button" tabindex="0" aria-label="Xem nhanh ${escapeHTML(product.name)}">
      <span class="${badgeClass}">${escapeHTML(product.category)}</span>${stockTag}
      <button class="fav-button${isFav ? ' active' : ''}" type="button" data-fav="${escapeHTML(product.id)}" aria-label="${isFav ? 'Bỏ yêu thích' : 'Lưu yêu thích'}" aria-pressed="${isFav}">${isFav ? '♥' : '♡'}</button>
      <img src="${escapeHTML(product.image)}" alt="${escapeHTML(product.name)}" loading="lazy" width="420" height="320">
    </div>
    <div class="product-body">
      <div class="product-kicker-row">
        <span class="product-kicker">${escapeHTML(product.label)}</span>
        ${ratingHtml}
      </div>
      <h3 class="product-title" data-detail="${escapeHTML(product.id)}">${escapeHTML(product.name)}</h3>
      <p class="product-description">${escapeHTML(product.description)}</p>
      <div class="product-bottom">
        <strong class="product-price${priceClass}">${price}</strong>
        <button class="detail-button" type="button" data-detail="${escapeHTML(product.id)}" aria-label="Xem chi tiết ${escapeHTML(product.name)}" title="Xem chi tiết">↗</button>
      </div>
      <div class="card-cta-row">
        <button class="add-button" type="button" data-add="${escapeHTML(product.id)}" ${!available ? 'disabled' : ''}>${!available ? statusText(product) || 'Giá đang cập nhật' : '<span aria-hidden="true">＋</span> Thêm vào giỏ'}</button>
        ${available ? `<button class="buy-now-icon-btn" type="button" data-buy-now="${escapeHTML(product.id)}" title="Mua ngay 1 chạm" aria-label="Mua ngay ${escapeHTML(product.name)}">⚡</button>` : ''}
      </div>
    </div>`;
  return article;
}

function renderProducts() {
  const found = getVisibleProducts();
  $('productGrid').replaceChildren(...found.map(productCard));
  $('resultCount').textContent = `${found.length} đầu sách phù hợp`;
  $('emptyState').hidden = found.length > 0;
}

function renderLiveSearchDropdown() {
  const box = $('searchDropdown');
  const q = normalize($('searchInput').value.trim());
  if (!box || !q) {
    if (box) box.hidden = true;
    return;
  }
  const matches = products
    .filter(p => normalize(`${p.name} ${p.category} ${p.label}`).includes(q))
    .slice(0, 5);
  if (!matches.length) {
    box.innerHTML = '<div class="search-dd-empty">Không tìm thấy sách khớp từ khóa</div>';
    box.hidden = false;
    return;
  }
  box.innerHTML = matches.map(p => {
    const sub = p.status === 'coming_soon' ? 'Sắp ra mắt' : (p.price ? money(p.price) : 'Liên hệ');
    return `<button type="button" class="search-dd-item" data-dd-id="${escapeHTML(p.id)}">
      <img src="${escapeHTML(p.image)}" alt="">
      <div><b>${escapeHTML(p.name)}</b><small>${escapeHTML(p.category)} · ${escapeHTML(sub)}</small></div>
    </button>`;
  }).join('');
  box.hidden = false;
}

function renderRecentlyViewed() {
  const wrap = $('recentlyViewedBox');
  const list = $('recentlyViewedList');
  if (!wrap || !list) return;
  const recentBooks = recentIds.map(id => products.find(p => p.id === id)).filter(Boolean);
  wrap.hidden = recentBooks.length === 0;
  if (!recentBooks.length) return;
  list.innerHTML = recentBooks.map(p => `
    <button type="button" class="recent-pill-card" data-recent-id="${escapeHTML(p.id)}">
      <img src="${escapeHTML(p.image)}" alt="">
      <div><b>${escapeHTML(p.name)}</b><small>${p.price ? money(p.price) : 'Sắp ra mắt'}</small></div>
    </button>
  `).join('');
}

function addToCart(id, silent = false) {
  const product = products.find((item) => item.id === id);
  if (!product || !isAvailable(product)) return false;
  const maxStock = Math.min(99, stockQtyOf(product));
  if ((cart[id] || 0) >= maxStock) {
    showToast(`Kho hiện chỉ còn tối đa ${maxStock} cuốn cho đầu sách này`);
    return false;
  }
  cart[id] = Math.min(maxStock, (cart[id] || 0) + 1);
  persistCart();
  if (!silent) showToast('Đã thêm sách vào giỏ hàng');
  return true;
}

async function buyNow(id) {
  const ok = addToCart(id, true);
  if (!ok && !cart[id]) return;
  await openCheckoutFlow();
}

function toggleWishlist(id) {
  if (wishlist.has(id)) {
    wishlist.delete(id);
    showToast('Đã bỏ khỏi danh sách đã lưu');
  } else {
    wishlist.add(id);
    showToast('Đã lưu vào danh sách yêu thích ♥');
  }
  persistWishlist();
  renderProducts();
}

function cartQuantity() {
  return Object.values(cart).reduce((sum, quantity) => sum + quantity, 0);
}

function cartSubtotal() {
  return products.reduce((sum, product) => sum + (product.price || 0) * (cart[product.id] || 0), 0);
}

function populateCheckoutAutofill(me) {
  if (!me || !me.authenticated) return;
  let filled = false;
  if ($('checkoutName') && !$('checkoutName').value.trim() && me.full_name) {
    $('checkoutName').value = me.full_name;
    filled = true;
  }
  if ($('checkoutPhone') && !$('checkoutPhone').value.trim() && me.phone) {
    $('checkoutPhone').value = me.phone;
    filled = true;
  }
  if ($('checkoutAddress') && !$('checkoutAddress').value.trim() && me.address) {
    $('checkoutAddress').value = me.address;
    filled = true;
  }
  if ($('autofillHint')) $('autofillHint').hidden = !filled;
}

function updateCheckoutTotals() {
  const subtotal = cartSubtotal();
  const discount = promosEnabled && activePromo ? Math.min(subtotal, activePromoDiscount) : 0;
  const ship = calcShipping(subtotal);
  const finalTotal = Math.max(0, subtotal - discount + ship);

  if ($('checkoutSubtotal')) $('checkoutSubtotal').textContent = money(subtotal);
  if ($('checkoutShipping')) $('checkoutShipping').textContent = ship === 0 ? 'Miễn phí' : money(ship);
  if ($('checkoutDiscountLine')) {
    $('checkoutDiscountLine').hidden = discount <= 0;
    if ($('checkoutDiscountVal')) $('checkoutDiscountVal').textContent = `-${money(discount)} (${activePromo})`;
  }
  $('checkoutTotal').textContent = money(finalTotal);

  // Render itemized order recap inside checkout dialog
  const lines = products.filter(p => cart[p.id] && isAvailable(p));
  if ($('checkoutItemsCount')) {
    $('checkoutItemsCount').textContent = `${cartQuantity()} cuốn sách trong đơn`;
  }
  if ($('checkoutItemsList')) {
    $('checkoutItemsList').innerHTML = lines.map(p => `
      <div class="recap-item-row">
        <span>${escapeHTML(p.name)} <b>×${cart[p.id]}</b></span>
        <strong>${money(p.price * cart[p.id])}</strong>
      </div>
    `).join('');
  }
}

function renderCart() {
  for (const id of Object.keys(cart)) {
    const book = products.find(x => x.id === id);
    if (!book || !isAvailable(book)) delete cart[id];
    else if (cart[id] > stockQtyOf(book)) cart[id] = stockQtyOf(book);
  }
  try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch {}
  const count = cartQuantity();
  const subtotal = cartSubtotal();
  const discount = promosEnabled && activePromo ? Math.min(subtotal, activePromoDiscount) : 0;
  const ship = calcShipping(subtotal);
  const finalTotal = Math.max(0, subtotal - discount + ship);

  $('cartCount').textContent = count;
  $('stickyCount').textContent = count;
  $('stickyTotal').textContent = money(finalTotal);
  $('cartSubtotal').textContent = money(subtotal);
  if ($('cartShipping')) $('cartShipping').textContent = subtotal === 0 ? '—' : (ship === 0 ? 'Miễn phí' : money(ship));
  $('cartTotal').textContent = money(finalTotal);
  $('stickyCart').hidden = count === 0;
  $('checkoutOpen').disabled = count === 0;
  if ($('cartClearBtn')) $('cartClearBtn').hidden = count === 0;

  if ($('cartDiscountRow')) {
    $('cartDiscountRow').hidden = discount <= 0;
    if (discount > 0) {
      $('cartPromoLabel').textContent = activePromo;
      $('cartDiscount').textContent = '-' + money(discount);
    }
  }

  if ($('shipProgressText') && $('shipProgressFill')) {
    const target = freeshipThreshold || 200000;
    const pct = Math.min(100, Math.round((subtotal / target) * 100));
    $('shipProgressFill').style.width = pct + '%';
    if (subtotal === 0) {
      $('shipProgressText').textContent = `Miễn phí vận chuyển cho đơn từ ${money(target)}`;
    } else if (subtotal >= target) {
      $('shipProgressText').innerHTML = '🎉 <b>Tuyệt vời!</b> Đơn hàng được Miễn phí vận chuyển';
    } else {
      $('shipProgressText').innerHTML = `Mua thêm <b>${money(target - subtotal)}</b> để được Miễn phí vận chuyển`;
    }
  }

  updateCheckoutTotals();

  const lines = products.filter((product) => cart[product.id] && isAvailable(product));
  if (!lines.length) {
    $('cartLines').innerHTML = '<div class="cart-empty"><span>▤</span><b>Giỏ sách đang trống</b><small>Hãy chọn một vài cuốn sách phù hợp cho lộ trình học tập nhé.</small></div>';
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

async function loadAndRenderReviews(bookId) {
  const container = $('detailReviewsList');
  if (!container) return;
  try {
    const reviews = await fetch(`/api/books/${encodeURIComponent(bookId)}/reviews`, { cache: 'no-store' }).then(r => r.ok ? r.json() : []);
    if (!reviews.length) {
      container.innerHTML = '<p class="muted-small">Chưa có nhận xét nào cho đầu sách này. Hãy là người đầu tiên chia sẻ cảm nhận!</p>';
      return;
    }
    container.innerHTML = reviews.map(rv => `
      <div class="review-item">
        <div class="review-item-head">
          <b>${escapeHTML(rv.author_name)}</b>
          ${rv.verified_purchase ? '<span class="verified-pill">✓ Đã mua sách</span>' : ''}
          <span class="review-stars">${'★'.repeat(rv.rating)}${'☆'.repeat(5 - rv.rating)}</span>
        </div>
        <p>${escapeHTML(rv.comment)}</p>
      </div>
    `).join('');
  } catch {
    container.innerHTML = '<p class="muted-small">Chưa tải được đánh giá.</p>';
  }
}

function showProductDetails(id) {
  const product = products.find((item) => item.id === id);
  if (!product) return;
  pushRecent(id);
  const available = isAvailable(product);
  const qty = stockQtyOf(product);
  const price = statusText(product) || (product.price === null ? 'Đang cập nhật' : money(product.price));
  const related = products
    .filter(p => p.id !== product.id && p.status !== 'coming_soon' && (p.category === product.category || isAvailable(p)))
    .slice(0, 3);

  $('productDialogContent').innerHTML = `
    <div class="product-detail-layout">
      <div class="product-detail-image"><img src="${escapeHTML(product.image)}" alt="${escapeHTML(product.name)}"></div>
      <div class="product-detail-copy">
        <div class="eyebrow"><span class="eyebrow-line"></span> ${escapeHTML(product.category.toUpperCase())} · ${escapeHTML(product.label || 'SÁCH THAM KHẢO')}</div>
        <h2 id="productDialogTitle">${escapeHTML(product.name)}</h2>
        <p>${escapeHTML(product.description)}</p>
        <div class="detail-price-row">
          <div class="detail-price">${price}</div>
          <span class="detail-stock-badge ${available ? 'in' : 'out'}">${product.status === 'coming_soon' ? 'Sắp phát hành' : available ? `Còn hàng (${qty} cuốn)` : 'Tạm hết hàng'}</span>
        </div>
        <div class="detail-meta">Giao hàng tận nơi · Miễn phí vận chuyển cho đơn từ ${money(freeshipThreshold)} · Hỗ trợ đổi trả nếu sách lỗi in ấn.</div>
        <div class="detail-cta-group">
          ${product.status === 'coming_soon'
            ? `<button class="button button-primary" type="button" data-detail-waitlist="${escapeHTML(product.id)}">🔔 Nhận thông báo khi mở bán</button>`
            : `<button class="button button-outline" type="button" data-detail-add="${escapeHTML(product.id)}" ${!available ? 'disabled' : ''}>＋ Thêm vào giỏ</button>
               <button class="button button-primary" type="button" data-detail-buynow="${escapeHTML(product.id)}" ${!available ? 'disabled' : ''}>⚡ Mua ngay <span>→</span></button>`}
        </div>
      </div>
    </div>
    <div class="detail-lower-grid">
      <div class="detail-reviews-section">
        <h4>Đánh giá từ độc giả ${product.review_count ? `(${product.rating_avg}★ · ${product.review_count})` : ''}</h4>
        <div id="detailReviewsList" class="reviews-scroll"><p class="muted-small">Đang tải nhận xét…</p></div>
        ${currentUser && currentUser.authenticated ? `
          <form id="detailReviewForm" class="review-form" data-book-id="${escapeHTML(product.id)}">
            <div class="review-form-row">
              <select name="rating" aria-label="Chọn số sao">
                <option value="5">★★★★★ (5/5 Rất hay)</option>
                <option value="4">★★★★☆ (4/5 Tốt)</option>
                <option value="3">★★★☆☆ (3/5 Ổn)</option>
                <option value="2">★★☆☆☆ (2/5 Trung bình)</option>
                <option value="1">★☆☆☆☆ (1/5 Cần cải thiện)</option>
              </select>
              <input name="comment" required minlength="3" maxlength="400" placeholder="Chia sẻ cảm nhận về nội dung, bài tập của sách…">
              <button class="button button-primary" type="submit" style="min-height:38px;padding:0 16px;font-size:12px">Gửi</button>
            </div>
          </form>
        ` : `<p class="muted-small" style="margin-top:8px"><a href="/login.html" style="color:var(--green-2);font-weight:600">Đăng nhập</a> để gửi đánh giá cho đầu sách này.</p>`}
      </div>
      ${related.length ? `
        <div class="detail-related-section">
          <h4>Gợi ý mua kèm cùng lộ trình</h4>
          <div class="related-mini-list">
            ${related.map(r => `
              <div class="related-mini-card">
                <img src="${escapeHTML(r.image)}" alt="">
                <div class="related-mini-info">
                  <b data-switch-detail="${escapeHTML(r.id)}">${escapeHTML(r.name)}</b>
                  <small>${r.price ? money(r.price) : 'Liên hệ'}</small>
                </div>
                ${isAvailable(r) ? `<button type="button" class="mini-add-btn" data-mini-add="${escapeHTML(r.id)}" title="Thêm nhanh vào giỏ">＋</button>` : ''}
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}
    </div>`;
  $('productDialog').showModal();
  loadAndRenderReviews(id);
}

function openWaitlistModal(bookId) {
  const book = products.find(p => p.id === bookId);
  if (!book || !$('waitlistDialog')) return;
  $('waitlistBookId').value = book.id;
  $('waitlistBookName').textContent = `Đầu sách: ${book.name} (${book.price ? money(book.price) : 'Giá đang cập nhật'})`;
  if (currentUser && currentUser.authenticated) {
    if (!$('waitlistName').value && currentUser.full_name) $('waitlistName').value = currentUser.full_name;
    if (!$('waitlistPhone').value && currentUser.phone) $('waitlistPhone').value = currentUser.phone;
  }
  $('waitlistDialog').showModal();
}

function renderComingSoon() {
  const section = $('comingSoonSection') || $('coming-soon');
  const container = $('comingSoonGrid');
  if (!section || !container) return;
  const upcoming = products.filter(p => p.status === 'coming_soon');
  section.hidden = upcoming.length === 0;
  container.replaceChildren(...upcoming.map(product => {
    const article = document.createElement('article');
    article.className = 'coming-soon-book';
    const image = document.createElement('img');
    image.src = product.image; image.alt = product.name; image.loading = 'lazy';
    const waitCnt = product.waitlist_count ? ` · ${product.waitlist_count} người đang chờ` : '';
    const details = document.createElement('div');
    details.innerHTML = `
      <span class="upcoming-tag">SẮP RA MẮT${escapeHTML(waitCnt)}</span>
      <h3>${escapeHTML(product.name)}</h3>
      <p>${escapeHTML(product.description)}</p>
      <strong class="upcoming-price">${product.price === null ? 'Đang cập nhật giá' : money(product.price)}</strong>
      <div class="upcoming-actions">
        <button type="button" class="waitlist-trigger-btn" data-waitlist="${escapeHTML(product.id)}">🔔 Nhận thông báo mở bán</button>
      </div>`;
    article.append(image, details);
    return article;
  }));
}

function updatePaymentPreview(method) {
  const preview = $('paymentPreview');
  const copy = $('paymentPreviewCopy');
  const qr = $('qrVisual');
  if (!preview || !copy) return;
  if (method === 'cod') { preview.hidden = true; return; }
  preview.hidden = false;
  qr.hidden = false;
  const amt = $('checkoutTotal') ? $('checkoutTotal').textContent : '';
  if (method === 'bank_qr') {
    copy.innerHTML = `<b>VietQR 24/7 (${escapeHTML(amt)})</b><small>Nội dung CK tự động theo mã đơn hàng sau khi xác nhận (chế độ mô phỏng đồ án).</small>`;
  } else if (method === 'momo') {
    copy.innerHTML = `<b>Ví MoMo (${escapeHTML(amt)})</b><small>Mô phỏng quét mã QR Ví điện tử MoMo nhanh chóng, an toàn.</small>`;
  } else if (method === 'vnpay') {
    copy.innerHTML = `<b>VNPAY-QR (${escapeHTML(amt)})</b><small>Mô phỏng thanh toán qua ứng dụng ngân hàng & thẻ nội địa/quốc tế.</small>`;
  }
}

function resetFilters() {
  activeCategory = 'Tất cả';
  activeGoal = 'all';
  activePriceRange = 'all';
  inStockOnly = false;
  wishlistOnly = false;
  if ($('catalogSearch')) $('catalogSearch').value = '';
  $('searchInput').value = '';
  $('sortSelect').value = 'featured';
  if ($('priceFilter')) $('priceFilter').value = 'all';
  if ($('inStockOnly')) $('inStockOnly').checked = false;
  if ($('advisorGoal')) $('advisorGoal').value = 'all';
  if ($('wishlistFilterBtn')) {
    $('wishlistFilterBtn').classList.remove('active');
    $('wishlistFilterBtn').setAttribute('aria-pressed', 'false');
  }
  if ($('searchDropdown')) $('searchDropdown').hidden = true;
  renderCategories();
  renderProducts();
}

async function applyPromoFromServer(code) {
  const clean = String(code || '').trim().toUpperCase();
  const fb = $('promoFeedback');
  if (!clean) {
    activePromo = '';
    activePromoDiscount = 0;
    if (fb) fb.hidden = true;
    renderCart();
    return;
  }
  try {
    const res = await fetch('/api/promo/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: clean, subtotal: cartSubtotal() }),
    }).then(r => r.json());
    if (!res.valid) {
      activePromo = '';
      activePromoDiscount = 0;
      if (fb) { fb.hidden = false; fb.className = 'promo-feedback error'; fb.textContent = res.error || 'Mã không hợp lệ'; }
    } else {
      activePromo = res.code;
      activePromoDiscount = res.discount;
      if ($('promoInput')) $('promoInput').value = res.code;
      if ($('checkoutPromoInput')) $('checkoutPromoInput').value = res.code;
      if (fb) { fb.hidden = false; fb.className = 'promo-feedback success'; fb.textContent = `Đã áp dụng mã ${res.code} (-${money(res.discount)})`; }
    }
  } catch {
    if (fb) { fb.hidden = false; fb.className = 'promo-feedback error'; fb.textContent = 'Không kiểm tra được mã ưu đãi'; }
  }
  renderCart();
}

async function openCheckoutFlow() {
  if (!cartQuantity()) return;
  try {
    const me = await fetch('/api/me', { credentials: 'same-origin' }).then(r => r.json());
    currentUser = me;
    if (!me.authenticated) {
      location.href = '/login.html?next=checkout';
      return;
    }
    if ($('cartDialog').open) $('cartDialog').close();
    if ($('productDialog').open) $('productDialog').close();
    if ($('checkoutPromoInput')) $('checkoutPromoInput').value = activePromo || '';
    populateCheckoutAutofill(me);
    updateCheckoutTotals();
    $('checkoutDialog').showModal();
  } catch {
    showToast('Không kết nối được hệ thống tài khoản.');
  }
}

function printReceiptSlip() {
  if (!lastOrderReceipt) { window.print(); return; }
  const r = lastOrderReceipt;
  const win = window.open('', '_blank', 'width=720,height=680');
  if (!win) { window.print(); return; }
  const rows = r.items.map(it => `<tr><td style="padding:8px 0;border-bottom:1px solid #e2e8f0">${escapeHTML(it.name)}</td><td style="text-align:center;border-bottom:1px solid #e2e8f0">${it.quantity}</td><td style="text-align:right;border-bottom:1px solid #e2e8f0">${money(it.price * it.quantity)}</td></tr>`).join('');
  win.document.write(`<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Phiếu đơn hàng ${escapeHTML(r.order_number)}</title>
    <style>body{font-family:system-ui,-apple-system,sans-serif;padding:32px;color:#0b1f2a;max-width:640px;margin:auto}h1{margin:0 0 4px;font-size:22px}table{width:100%;border-collapse:collapse;margin:18px 0}th{text-align:left;border-bottom:2px solid #091d28;padding-bottom:8px;font-size:12px}.tot{font-size:18px;font-weight:700;color:#057699;text-align:right;margin-top:12px}</style>
    </head><body>
    <h1>LTD's Book Store — Phiếu xác nhận đơn hàng</h1>
    <p style="color:#64748b;font-size:13px">Mã đơn: <b>${escapeHTML(r.order_number)}</b> · Thanh toán: ${escapeHTML(r.payment_label)}</p>
    <p style="font-size:13px">Người nhận: <b>${escapeHTML(r.customer_name)}</b> (${escapeHTML(r.phone)})<br>Địa chỉ: ${escapeHTML(r.address)}</p>
    <table><thead><tr><th>Đầu sách</th><th style="text-align:center">SL</th><th style="text-align:right">Thành tiền</th></tr></thead><tbody>${rows}</tbody></table>
    <div class="tot">Tổng thanh toán: ${money(r.total)}</div>
    <script>window.onload=()=>{window.print();}<\/script></body></html>`);
  win.document.close();
}

async function refreshBooksFromServer() {
  try {
    let response = await fetch('/api/books', { cache: 'no-store' }).catch(() => null);
    if (!response || !response.ok) response = await fetch('catalog.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Không tải được danh mục sách.');
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error('Dữ liệu danh mục không hợp lệ.');
    products = data.filter((item) => item && typeof item.id === 'string' && typeof item.name === 'string' && typeof item.image === 'string');
    return true;
  } catch (error) {
    $('productGrid').innerHTML = '<div class="empty-state"><h3>Chưa thể tải danh mục sách</h3><p>Hãy chạy website thông qua máy chủ theo hướng dẫn trong README.</p></div>';
    $('resultCount').textContent = 'Lỗi tải dữ liệu';
    console.error(error);
    return false;
  }
}

async function loadSiteConfig() {
  try {
    const cfg = await fetch('/api/site-config', { cache: 'no-store' }).then(r => r.ok ? r.json() : null);
    if (!cfg) return;
    if (cfg.theme_preset) document.documentElement.dataset.theme = cfg.theme_preset;
    if (cfg.contact_name && $('contactNameVal')) $('contactNameVal').textContent = cfg.contact_name;
    if (cfg.contact_phone && $('contactPhoneVal')) $('contactPhoneVal').textContent = cfg.contact_phone;
    if (cfg.contact_note && $('contactNoteVal')) $('contactNoteVal').textContent = cfg.contact_note;
    if (cfg.contact_phone && $('benefitContact')) $('benefitContact').textContent = `Hotline: ${cfg.contact_phone}`;
    if ($('advisorBox')) $('advisorBox').hidden = cfg.show_advisor === false;
    if ($('coming-soon') && cfg.show_coming_soon === false) $('coming-soon').hidden = true;

    shippingEnabled = Boolean(cfg.enable_shipping_fee);
    freeshipThreshold = Number(cfg.freeship_threshold || 200000);
    baseShippingFee = Number(cfg.shipping_fee || 25000);
    if ($('activeFilterSummary')) {
      $('activeFilterSummary').textContent = `MIỄN PHÍ VẬN CHUYỂN ĐƠN TỪ ${money(freeshipThreshold).toUpperCase()}`;
    }

    if (Array.isArray(cfg.categories) && cfg.categories.length) {
      categories = ['Tất cả', ...cfg.categories.filter(c => c !== 'Tất cả')];
      renderCategories();
    }

    promosEnabled = Boolean(cfg.enable_promos);
    if ($('promoBox')) $('promoBox').hidden = !promosEnabled;
    if (promosEnabled && $('promoChips') && Array.isArray(cfg.public_promos)) {
      $('promoChips').innerHTML = cfg.public_promos.map(pr => {
        const desc = pr.type === 'percent' ? `-${pr.value}%` : `-${money(pr.value)}`;
        return `<button type="button" class="promo-chip" data-promo="${escapeHTML(pr.code)}">${escapeHTML(pr.code)} (${desc})</button>`;
      }).join('');
      $('promoChips').querySelectorAll('.promo-chip').forEach(chip => {
        chip.addEventListener('click', () => applyPromoFromServer(chip.dataset.promo));
      });
    }
  } catch {}
}

async function loadBanner() {
  try {
    const b = await fetch('/api/banner', { cache: 'no-store' }).then(r => r.ok ? r.json() : null);
    if (!b) return;
    if ($('announcementText') && b.announcement_text) $('announcementText').textContent = b.announcement_text;
    if ($('heroEyebrow') && b.hero_eyebrow) $('heroEyebrow').textContent = b.hero_eyebrow;
    if ($('heroTitle') && b.hero_title_line1) {
      $('heroTitle').innerHTML = `${escapeHTML(b.hero_title_line1)}<br><span>${escapeHTML(b.hero_title_highlight || '')}</span>`;
    }
    if ($('heroDesc') && b.hero_description) $('heroDesc').textContent = b.hero_description;
    if ($('heroSticker') && b.hero_sticker_top) {
      $('heroSticker').innerHTML = `${escapeHTML(b.hero_sticker_top)}<br><b>${escapeHTML(b.hero_sticker_bottom || '')}</b>`;
    }
    if ($('heroNoteTitle') && b.hero_note_title) $('heroNoteTitle').textContent = b.hero_note_title;
    if ($('heroNoteSub') && b.hero_note_sub) $('heroNoteSub').textContent = b.hero_note_sub;
    if ($('comingSoonEyebrow') && b.coming_soon_eyebrow) $('comingSoonEyebrow').textContent = b.coming_soon_eyebrow;
    if ($('comingSoonTitle') && b.coming_soon_title) {
      $('comingSoonTitle').innerHTML = `${escapeHTML(b.coming_soon_title)} <span>${escapeHTML(b.coming_soon_highlight || '')}</span>`;
    }
    if ($('comingSoonDesc') && b.coming_soon_description) $('comingSoonDesc').textContent = b.coming_soon_description;
  } catch {}
}

async function init() {
  await Promise.all([loadSiteConfig(), loadBanner()]);
  const ok = await refreshBooksFromServer();
  if (!ok) return;

  try {
    const me = await fetch('/api/me').then(r => r.json());
    currentUser = me;
    if (me.authenticated) {
      const link = $('accountLink');
      if (link) {
        link.textContent = me.role === 'admin' ? '🎛️ Quản trị' : '👤 ' + (me.full_name || me.username);
        link.href = me.role === 'admin' ? '/admin.html' : '/account.html';
      }
    }
  } catch {}

  loadCart();
  loadWishlist();
  loadRecent();
  persistWishlist();
  renderCategories();
  renderProducts();
  renderComingSoon();
  renderRecentlyViewed();
  renderCart();

  $('categoryTabs').addEventListener('keydown', (event) => {
    if (event.key === 'Escape') $('searchInput').focus();
  });

  $('productGrid').addEventListener('click', (event) => {
    const favBtn = event.target.closest('[data-fav]');
    if (favBtn) { event.stopPropagation(); toggleWishlist(favBtn.dataset.fav); return; }
    const buyBtn = event.target.closest('[data-buy-now]');
    if (buyBtn) { event.stopPropagation(); buyNow(buyBtn.dataset.buyNow); return; }
    const addButton = event.target.closest('[data-add]');
    if (addButton) { addToCart(addButton.dataset.add); return; }
    const detailTrigger = event.target.closest('[data-detail]');
    if (detailTrigger) showProductDetails(detailTrigger.dataset.detail);
  });

  if ($('comingSoonGrid')) {
    $('comingSoonGrid').addEventListener('click', (e) => {
      const btn = e.target.closest('[data-waitlist]');
      if (btn) openWaitlistModal(btn.dataset.waitlist);
    });
  }

  if ($('recentlyViewedList')) {
    $('recentlyViewedList').addEventListener('click', (e) => {
      const card = e.target.closest('[data-recent-id]');
      if (card) showProductDetails(card.dataset.recentId);
    });
  }
  if ($('clearRecentBtn')) {
    $('clearRecentBtn').addEventListener('click', () => {
      recentIds = [];
      try { localStorage.removeItem(RECENT_KEY); } catch {}
      renderRecentlyViewed();
    });
  }

  if ($('advisorGoal')) {
    $('advisorGoal').addEventListener('change', (e) => {
      activeGoal = e.target.value;
      if (activeGoal === 'exam10' && categories.includes('Ôn thi lớp 10')) activeCategory = 'Ôn thi lớp 10';
      else if (activeGoal === 'all') activeCategory = 'Tất cả';
      renderCategories();
      renderProducts();
    });
  }

  if ($('priceFilter')) {
    $('priceFilter').addEventListener('change', (e) => {
      activePriceRange = e.target.value;
      renderProducts();
    });
  }
  if ($('inStockOnly')) {
    $('inStockOnly').addEventListener('change', (e) => {
      inStockOnly = e.target.checked;
      renderProducts();
    });
  }

  if ($('wishlistFilterBtn')) {
    $('wishlistFilterBtn').addEventListener('click', () => {
      wishlistOnly = !wishlistOnly;
      $('wishlistFilterBtn').classList.toggle('active', wishlistOnly);
      $('wishlistFilterBtn').setAttribute('aria-pressed', String(wishlistOnly));
      renderProducts();
    });
  }

  if ($('promoApplyBtn')) {
    $('promoApplyBtn').addEventListener('click', () => applyPromoFromServer($('promoInput').value));
  }

  if ($('paymentMethods')) {
    $('paymentMethods').addEventListener('change', (e) => {
      const radio = e.target.closest('input[name="payment_method"]');
      if (!radio) return;
      document.querySelectorAll('.payment-option').forEach(opt => opt.classList.toggle('selected', opt.querySelector('input').checked));
      updatePaymentPreview(radio.value);
    });
  }

  $('productDialogContent').addEventListener('click', (event) => {
    const addBtn = event.target.closest('[data-detail-add]');
    if (addBtn) { addToCart(addBtn.dataset.detailAdd); $('productDialog').close(); return; }
    const buyBtn = event.target.closest('[data-detail-buynow]');
    if (buyBtn) { buyNow(buyBtn.dataset.detailBuynow); return; }
    const waitBtn = event.target.closest('[data-detail-waitlist]');
    if (waitBtn) { $('productDialog').close(); openWaitlistModal(waitBtn.dataset.detailWaitlist); return; }
    const switchBtn = event.target.closest('[data-switch-detail]');
    if (switchBtn) { showProductDetails(switchBtn.dataset.switchDetail); return; }
    const miniAdd = event.target.closest('[data-mini-add]');
    if (miniAdd) { addToCart(miniAdd.dataset.miniAdd); }
  });

  $('productDialogContent').addEventListener('submit', async (event) => {
    const form = event.target.closest('#detailReviewForm');
    if (!form) return;
    event.preventDefault();
    const bookId = form.dataset.bookId;
    const fd = new FormData(form);
    try {
      const res = await fetch(`/api/books/${encodeURIComponent(bookId)}/reviews`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', ...(currentUser?.csrf ? { 'X-CSRF-Token': currentUser.csrf } : {}) },
        body: JSON.stringify({ rating: Number(fd.get('rating')), comment: String(fd.get('comment')).trim() }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || 'Không thể gửi đánh giá');
      form.reset();
      showToast('Cảm ơn bạn đã gửi đánh giá sách! ★');
      await refreshBooksFromServer();
      renderProducts();
      loadAndRenderReviews(bookId);
    } catch (err) {
      showToast(err.message || 'Lỗi khi gửi đánh giá');
    }
  });

  if ($('waitlistForm')) {
    $('waitlistClose').addEventListener('click', () => $('waitlistDialog').close());
    $('waitlistDialog').addEventListener('click', (e) => { if (e.target === $('waitlistDialog')) $('waitlistDialog').close(); });
    $('waitlistForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(e.currentTarget);
      const btn = $('waitlistSubmitBtn');
      btn.disabled = true;
      try {
        const res = await fetch('/api/waitlist', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            book_id: String(fd.get('book_id')),
            customer_name: String(fd.get('customer_name')).trim(),
            phone: String(fd.get('phone')).trim(),
            note: String(fd.get('note') || '').trim(),
          }),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.detail || 'Không thể đăng ký nhận thông báo');
        $('waitlistDialog').close();
        showToast(data.message || 'Đã đăng ký nhận thông báo mở bán!');
        await refreshBooksFromServer();
        renderComingSoon();
      } catch (err) {
        showToast(err.message || 'Lỗi kết nối máy chủ');
      } finally {
        btn.disabled = false;
      }
    });
  }

  $('cartLines').addEventListener('click', (event) => {
    const button = event.target.closest('[data-quantity]');
    if (!button) return;
    const { id, quantity: action } = button.dataset;
    const book = products.find(p => p.id === id);
    const maxQ = book ? Math.min(99, stockQtyOf(book)) : 99;
    if (action === 'remove') delete cart[id];
    else if (action === 'plus') {
      if ((cart[id] || 0) >= maxQ) showToast(`Kho chỉ còn ${maxQ} cuốn`);
      cart[id] = Math.min(maxQ, (cart[id] || 0) + 1);
    } else if (action === 'minus') {
      cart[id] = (cart[id] || 0) - 1;
      if (cart[id] <= 0) delete cart[id];
    }
    persistCart();
    if (activePromo) applyPromoFromServer(activePromo);
  });

  if ($('cartClearBtn')) {
    $('cartClearBtn').addEventListener('click', () => {
      cart = {};
      activePromo = '';
      activePromoDiscount = 0;
      persistCart();
      showToast('Đã làm trống giỏ sách');
    });
  }

  $('searchInput').addEventListener('input', () => {
    if ($('catalogSearch')) $('catalogSearch').value = $('searchInput').value;
    renderProducts();
    renderLiveSearchDropdown();
  });
  $('searchInput').addEventListener('focus', renderLiveSearchDropdown);
  if ($('searchDropdown')) {
    $('searchDropdown').addEventListener('click', (e) => {
      const item = e.target.closest('[data-dd-id]');
      if (!item) return;
      $('searchDropdown').hidden = true;
      showProductDetails(item.dataset.ddId);
    });
  }
  document.addEventListener('click', (e) => {
    if ($('searchDropdown') && !e.target.closest('.header-search-wrap')) {
      $('searchDropdown').hidden = true;
    }
  });
  document.addEventListener('keydown', (event) => {
    const target = event.target;
    const editing = target && (target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName));
    if (event.key === '/' && !editing) { event.preventDefault(); $('searchInput').focus(); }
    if (event.key === 'Escape' && $('searchDropdown')) $('searchDropdown').hidden = true;
  });

  if ($('catalogSearch')) {
    $('catalogSearch').addEventListener('input', () => {
      $('searchInput').value = $('catalogSearch').value;
      renderProducts();
    });
  }

  $('sortSelect').addEventListener('change', renderProducts);
  $('clearFilters').addEventListener('click', (event) => { event.preventDefault(); resetFilters(); });
  $('resetSearch').addEventListener('click', resetFilters);
  $('cartOpen').addEventListener('click', () => $('cartDialog').showModal());
  $('stickyCartOpen').addEventListener('click', () => $('cartDialog').showModal());
  if ($('stickyCheckoutNow')) $('stickyCheckoutNow').addEventListener('click', openCheckoutFlow);
  $('cartClose').addEventListener('click', () => $('cartDialog').close());
  $('cartDialog').addEventListener('click', (event) => { if (event.target === $('cartDialog')) $('cartDialog').close(); });
  $('productDialogClose').addEventListener('click', () => $('productDialog').close());
  $('productDialog').addEventListener('click', (event) => { if (event.target === $('productDialog')) $('productDialog').close(); });
  $('checkoutClose').addEventListener('click', () => $('checkoutDialog').close());
  if ($('backToCartBtn')) {
    $('backToCartBtn').addEventListener('click', () => {
      $('checkoutDialog').close();
      $('cartDialog').showModal();
    });
  }

  $('checkoutOpen').addEventListener('click', openCheckoutFlow);

  $('checkoutForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!cartQuantity()) return;
    const form = event.currentTarget;
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      const me = await fetch('/api/me', { credentials: 'same-origin' }).then(r => r.json());
      currentUser = me;
      if (!me.authenticated) { location.href = '/login.html?next=checkout'; return; }
      const data = new FormData(form);
      const snapshotItems = products
        .filter(p => cart[p.id] && isAvailable(p))
        .map(p => ({ book_id: p.id, name: p.name, price: p.price, quantity: cart[p.id] }));
      const payload = {
        customer_name: String(data.get('name')).trim(),
        phone: String(data.get('phone')).trim(),
        address: String(data.get('address')).trim(),
        note: String(data.get('note') || '').trim(),
        payment_method: String(data.get('payment_method') || 'cod'),
        promo_code: promosEnabled ? activePromo : '',
        items: snapshotItems.map(({ book_id, quantity }) => ({ book_id, quantity })),
      };
      const response = await fetch('/api/orders', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': me.csrf },
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(typeof result.detail === 'string' ? result.detail : 'Không thể ghi nhận đơn hàng');

      lastOrderReceipt = {
        order_number: result.order_number,
        payment_label: result.payment_label || 'COD',
        customer_name: payload.customer_name,
        phone: payload.phone,
        address: payload.address,
        total: result.total,
        items: snapshotItems,
      };

      cart = {};
      activePromo = '';
      activePromoDiscount = 0;
      if ($('promoInput')) $('promoInput').value = '';
      if ($('promoFeedback')) $('promoFeedback').hidden = true;
      await refreshBooksFromServer();
      renderProducts();
      persistCart();
      document.querySelectorAll('.payment-option').forEach((opt, i) => opt.classList.toggle('selected', i === 0));
      updatePaymentPreview('cod');
      $('checkoutDialog').close();

      const discountNote = result.discount_amount > 0 ? `<div class="rc-row"><span>Ưu đãi (${escapeHTML(result.promo_code)})</span><b>-${money(result.discount_amount)}</b></div>` : '';
      const shipNote = `<div class="rc-row"><span>Vận chuyển</span><b>${result.shipping_fee > 0 ? money(result.shipping_fee) : 'Miễn phí'}</b></div>`;
      $('receiptSummary').innerHTML = `
        <div class="rc-row"><span>Mã đơn hàng</span><b>${escapeHTML(result.order_number)}</b></div>
        <div class="rc-row"><span>Người nhận</span><b>${escapeHTML(payload.customer_name)} · ${escapeHTML(payload.phone)}</b></div>
        <div class="rc-row"><span>Phương thức</span><b>${escapeHTML(result.payment_label || 'COD')}</b></div>
        ${shipNote}${discountNote}
        <div class="rc-row total"><span>Tổng thanh toán</span><strong>${money(result.total)}</strong></div>`;
      $('receiptDialog').showModal();
    } catch (error) {
      showToast(error.message || 'Đã có lỗi, vui lòng thử lại');
    } finally { button.disabled = false; }
  });

  if ($('receiptPrintBtn')) $('receiptPrintBtn').addEventListener('click', printReceiptSlip);
  $('receiptClose').addEventListener('click', () => $('receiptDialog').close());

  const urlParams = new URLSearchParams(location.search);
  if (urlParams.get('openCart') === '1') {
    history.replaceState({}, '', location.pathname + location.hash);
    if (cartQuantity()) $('cartDialog').showModal();
  } else if (urlParams.get('checkout') === '1') {
    history.replaceState({}, '', location.pathname + location.hash);
    if (cartQuantity()) openCheckoutFlow();
  }

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

// Dark/Light Mode, Hero Parallax, Back-to-Top
(function setupArtEdition() {
  const MODE_KEY = 'ltd-book-store-mode';
  const btn = $('themeModeBtn');
  const applyMode = (mode) => {
    document.documentElement.dataset.mode = mode;
    if (btn) btn.textContent = mode === 'dark' ? '☀' : '☾';
  };
  try {
    const saved = localStorage.getItem(MODE_KEY);
    if (saved === 'dark' || saved === 'light') applyMode(saved);
  } catch {}
  if (btn) {
    btn.addEventListener('click', () => {
      const next = document.documentElement.dataset.mode === 'dark' ? 'light' : 'dark';
      applyMode(next);
      try { localStorage.setItem(MODE_KEY, next); } catch {}
    });
  }

  const topBtn = $('backToTop');
  if (topBtn) {
    window.addEventListener('scroll', () => {
      topBtn.hidden = window.scrollY < 420;
    }, { passive: true });
    topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  const heroArt = document.querySelector('.hero-art');
  if (heroArt && window.matchMedia('(prefers-reduced-motion: reduce)').matches === false) {
    heroArt.addEventListener('mousemove', (e) => {
      const r = heroArt.getBoundingClientRect();
      const dx = ((e.clientX - r.left) / r.width - 0.5) * 10;
      const dy = ((e.clientY - r.top) / r.height - 0.5) * 8;
      heroArt.style.transform = `perspective(900px) rotateY(${dx * 0.45}deg) rotateX(${-dy * 0.45}deg)`;
    });
    heroArt.addEventListener('mouseleave', () => {
      heroArt.style.transform = '';
    });
  }
})();
