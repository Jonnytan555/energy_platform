from fastapi import FastAPI
from app.storage.storage_router import router as storage_router
from app.curves.curve_router import router as curve_router
from app.regression.regression_router import router as regression_router
from app.routers import users, auth

app = FastAPI(title="Energy API", version="1.1")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(storage_router)
app.include_router(curve_router)
app.include_router(regression_router)

@app.get("/")
async def root():
    return {"message": "Energy API running with Storage + Curves + Regression"}
