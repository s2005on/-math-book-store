const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const web = path.resolve(__dirname, '..', 'server', 'web');
const catalog = JSON.parse(fs.readFileSync(path.join(web, 'catalog.json'), 'utf8'));

test('catalog has unique IDs and required product fields', () => {
  const ids = catalog.map((item) => item.id);
  assert.equal(new Set(ids).size, ids.length);
  for (const item of catalog) {
    assert.ok(item.id && item.name && item.category && item.image && item.description);
    assert.ok(item.price === null || (Number.isInteger(item.price) && item.price > 0));
  }
});

test('all catalog image references exist', () => {
  for (const item of catalog) assert.ok(fs.existsSync(path.join(web, item.image)), item.image);
});

test('sample price data is consistent', () => {
  const prices = Object.fromEntries(catalog.map((item) => [item.id, item.price]));
  assert.equal(prices.math6, 80000);
  assert.equal(prices.math7, 80000);
  assert.equal(prices.math8, 80000);
  assert.equal(prices.math9, 80000);
  assert.equal(prices.entrance, 270000);
  assert.equal(prices.hsg8, 198000);
  assert.equal(prices['63de'], null);
});

test('storefront references catalog, CSS and JavaScript', () => {
  const html = fs.readFileSync(path.join(web, 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(web, 'app.js'), 'utf8');
  assert.match(html, /styles\.css/);
  assert.match(html, /app\.js/);
  assert.match(js, /fetch\('catalog\.json'/);
});
