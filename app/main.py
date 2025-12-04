from fastapi import FastAPI
from app.routers import (
    curves_router,
    storage_router,
    shipping_router,
    lng_router,
    market_router,
)

app = FastAPI(
    title="Energy Analytics Platform",
    version="1.0.0",
    description="Full API for gas, LNG, curves, shipping, and market analytics."
)

app.include_router(curves_router)
app.include_router(storage_router)
app.include_router(shipping_router)
app.include_router(lng_router)
app.include_router(market_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Energy Analytics Platform API running"}
