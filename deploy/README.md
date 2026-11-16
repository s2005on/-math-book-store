# Deploy LTD's Book Store

VPS is managed by the project owner. These files are templates; set the real domain, user, paths and TLS before use.

1. Copy the repository to /opt/ltds-book-store.
2. Create a virtual environment and install server/requirements.txt.
3. Run uvicorn server.app:app on 127.0.0.1:8017.
4. Configure Nginx reverse proxy using nginx-location.conf and enable HTTPS.
5. Install ltds-book-store.service after reviewing User, WorkingDirectory and ExecStart.
6. Verify /health and the storefront from the public domain.

The current build is static UI only. Do not accept real orders until database, authentication, server-side validation, order APIs, logging, backups and privacy controls are implemented and tested.
