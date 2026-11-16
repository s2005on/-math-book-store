# Runtime Configuration

## Local defaults
- Host: 127.0.0.1
- Port: 8017
- Static web root: server/web
- Catalog: server/web/catalog.json
- Cart storage: browser localStorage

## Production guidance
Place the app behind Nginx and HTTPS. Keep Uvicorn bound to localhost. Do not add secrets to source control. The current UI-only version does not require database credentials or payment keys.
