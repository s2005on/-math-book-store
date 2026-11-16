# Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Prices or book details are outdated | High | Confirm with seller before public sale |
| Demo checkout mistaken for real order | High | Prominent demo notice; no backend submission |
| Browser localStorage is cleared | Medium | Explain cart is device/browser-local |
| Missing or broken book-cover asset | Medium | Catalog test checks every image path |
| Admin preview mistaken for secure admin | High | Label preview; implement auth before CRUD |
| VPS misconfiguration or exposed app port | High | Nginx reverse proxy, HTTPS and localhost bind |
| Scope grows before deadline | Medium | Prioritize backlog by lecturer rubric |
