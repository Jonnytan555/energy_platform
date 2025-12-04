from fastapi import APIRouter
from app.storage.agsi_client import fetch_agsi_timeseries
from app.storage.asli_client import fetch_alsi_timeseries

router = APIRouter(prefix="/storage", tags=["storage"])

@router.get("/agsi")
async def get_agsi(country: str = "EU"):
    df = await fetch_agsi_timeseries(country=country)
    return df.to_dict(orient="records")

@router.get("/alsi")
async def get_asli(country: str = "EU"):
    df = await fetch_alsi_timeseries(country=country)
    return df.to_dict(orient="records")

