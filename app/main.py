import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator

from app.startup.scraper_registry import register_scrapers
from app.config import settings

register_scrapers()

from app.routers import auth_router, health_router, storage_router, users_router

app = FastAPI(
    title="Energy Analytics Platform",
    version="1.0.0",
    description="Full API for gas, LNG, curves, shipping, and market analytics.",
)

# --- Prometheus metrics ---
Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",         # Prometheus will scrape this
    include_in_schema=False,     # don't show in /docs
)

# --- Celery tasks router (only when enabled) ---
if getattr(settings, "CELERY_ENABLED", False):
    from app.routers import tasks_router
    app.include_router(tasks_router, prefix="/tasks")

# --- normal routers ---
app.include_router(storage_router)
app.include_router(auth_router)
app.include_router(health_router)

# --- CORS ---
origins = os.getenv("CORS_ORIGINS", "http://localhost").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),  # type: ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Optional React static mount (only if dist exists) ---
FRONTEND_DIST = "frontend/dist"
if os.path.isdir(FRONTEND_DIST):
    app.mount(
        "/web",
        StaticFiles(directory=FRONTEND_DIST, html=True),
        name="frontend",
    )
    print("✅ Mounted frontend from", FRONTEND_DIST)
else:
    print(f"ℹ️ Skipping static mount: {FRONTEND_DIST} not found in API image")

@app.get("/")
def root():
    return {"status": "ok", "message": "Energy Analytics Platform API running"}
