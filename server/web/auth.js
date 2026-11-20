'use strict';
(() => {
  const card = document.querySelector('[data-mode]');
  if (!card) return;
  const mode = card.dataset.mode;
  const form = document.getElementById('authForm');
  const message = document.getElementById('authMessage');
  const submit = document.getElementById('authSubmit');
  const isRegister = mode === 'register';
  const params = new URLSearchParams(location.search);
  const next = params.get('next') === 'checkout' ? 'checkout' : '';
  const other = document.getElementById('otherAction');
  const tabs = document.querySelectorAll('[data-login-link], [data-register-link]');
  tabs.forEach(link => {
    const target = link.hasAttribute('data-login-link') ? 'login.html' : 'register.html';
    link.href = '/' + target + (next ? '?next=checkout' : '');
  });
  if (other) other.href = '/' + (isRegister ? 'login.html' : 'register.html') + (next ? '?next=checkout' : '');
  const showFeedback = (text, success = false) => {
    message.textContent = text;
    message.classList.toggle('success', success);
  };
  if (!isRegister && params.get('registered') === '1') {
    showFeedback('Tài khoản đã tạo thành công! Hãy đăng nhập.', true);
  }
  document.querySelectorAll('[data-reveal]').forEach(button => {
    const field = document.getElementById(button.dataset.reveal);
    button.addEventListener('click', () => {
      const show = field.type === 'password';
      field.type = show ? 'text' : 'password';
      button.setAttribute('aria-pressed', String(show));
      button.setAttribute('aria-label', show ? 'Ẩn mật khẩu' : 'Hiện mật khẩu');
      field.focus({ preventScroll: true });
    });
  });
  const phoneInput = document.getElementById('phone');
  if (phoneInput) phoneInput.addEventListener('input', () => phoneInput.setCustomValidity(''));
  if (phoneInput) phoneInput.addEventListener('blur', () => {
    const value = phoneInput.value.trim().replace(/[ .-]/g, '');
    phoneInput.setCustomValidity(value && !/^0[35789][0-9]{8}$/.test(value) ? 'Số điện thoại Việt Nam phải có 10 chữ số, bắt đầu bằng 03, 05, 07, 08 hoặc 09.' : '');
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    showFeedback('');
    if (isRegister) {
      const phone = phoneInput.value.trim().replace(/[ .-]/g, '');
      if (!/^0[35789][0-9]{8}$/.test(phone)) {
        showFeedback('Số điện thoại phải có 10 chữ số, bắt đầu bằng 03, 05, 07, 08 hoặc 09.');
        phoneInput.focus();
        return;
      }
      if (form.elements.password.value !== form.elements.confirm_password.value) {
        showFeedback('Mật khẩu nhập lại chưa trùng khớp.');
        form.elements.confirm_password.focus();
        return;
      }
    }
    submit.disabled = true;
    const originalLabel = submit.querySelector('[data-submit-text]').textContent;
    submit.querySelector('[data-submit-text]').textContent = 'Đang xử lý…';
    try {
      const username = form.elements.username.value.trim().toLowerCase();
      const password = form.elements.password.value;
      const body = { username, password };
      if (isRegister) {
        body.full_name = form.elements.full_name.value.trim().replace(/\s+/g, ' ');
        body.phone = phoneInput.value.trim().replace(/[ .-]/g, '');
      }
      const response = await fetch(isRegister ? '/api/register' : '/api/login', {
        method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
      });
      const data = await response.json();
      if (!response.ok) {
        let detail = data.detail || 'Không thể thực hiện yêu cầu.';
        if (Array.isArray(detail)) detail = 'Vui lòng kiểm tra các thông tin đã nhập.';
        throw new Error(detail);
      }
      if (isRegister) {
        // Auto-login seamlessly right after registration so user doesn't have to re-type credentials
        const loginRes = await fetch('/api/login', {
          method: 'POST', credentials: 'same-origin',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password }),
        }).catch(() => null);
        if (loginRes && loginRes.ok) {
          location.assign(next ? '/?checkout=1' : '/account.html');
          return;
        }
        location.assign('/login.html?' + new URLSearchParams({ ...(next ? { next } : {}), registered: '1' }).toString());
      } else {
        location.assign(data.role === 'admin' ? '/admin.html' : (next ? '/?checkout=1' : '/account.html'));
      }
    } catch (error) {
      showFeedback(error instanceof Error ? error.message : 'Không thể kết nối máy chủ.');
    } finally {
      submit.disabled = false;
      submit.querySelector('[data-submit-text]').textContent = originalLabel;
    }
  });
  fetch('/api/me', { credentials: 'same-origin' })
    .then(response => response.ok ? response.json() : null)
    .then(data => {
      if (data && data.authenticated) location.replace(data.role === 'admin' ? '/admin.html' : (next ? '/?checkout=1' : '/account.html'));
    }).catch(() => {});
})();
