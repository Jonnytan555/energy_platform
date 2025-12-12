from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.startup.scraper_registry import register_scrapers

register_scrapers()

from app.routers import auth_router, storage_router, users_router

app = FastAPI(
    title="Energy Analytics Platform",
    version="1.0.0",
    description="Full API for gas, LNG, curves, shipping, and market analytics.",
)

app.include_router(storage_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/web",
    StaticFiles(directory="frontend/dist", html=True),
    name="frontend",
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Energy Analytics Platform API running"}
