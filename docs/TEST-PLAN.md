# Test Plan

## Scope
Storefront static hosting, catalog loading, image references, product search/filter/sort, cart demo and admin preview.

## Automated checks
- Python smoke tests: /health, storefront, admin preview, catalog JSON and image paths.
- Node tests: unique product IDs, required fields, valid sample prices, image files and asset references.
- Syntax: node --check server/web/app.js.

## Manual scenarios
1. Desktop and mobile navigation.
2. Search with and without Vietnamese diacritics.
3. Filter by class and reset filters.
4. Sort by price and name.
5. Add, increment, decrement and remove cart lines.
6. Verify zero-price/unknown-price item cannot be added.
7. Submit demo checkout and verify explicit demo message.

## Not covered
Production security, real order persistence, payment, inventory concurrency, email/SMS and VPS recovery.
