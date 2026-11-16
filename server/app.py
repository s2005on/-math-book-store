"""Static storefront host for Math Book Store UI Foundation."""
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

HERE = Path(__file__).resolve().parent
WEB = HERE / "web"
app = FastAPI(title="Math Book Store", docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/health", include_in_schema=False)
def health():
    return JSONResponse({"status": "ok", "project": "math-book-store", "stage": "ui-foundation", "api_ready": False})


app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
