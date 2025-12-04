from fastapi import FastAPI

from app.storage.storage_router import router as storage_router
from app.curves.curves_router import router as curves_router
from app.regression.regression_router import router as regression_router
from app.shipping.shipping_router import router as shipping_router
from app.market.market_router import router as market_router
from app.lng.lng_router import router as lng_router

app = FastAPI(
    title="Energy Analytics Platform",
    version="0.1.0"
)

app.include_router(storage_router)
app.include_router(curves_router)
app.include_router(regression_router)
app.include_router(shipping_router)
app.include_router(market_router)
app.include_router(lng_router)


@app.get("/")
def root():
    return {"message": "Energy Platform Running"}
