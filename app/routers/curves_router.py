from fastapi import APIRouter
from app.curves.builder import build_curve

router = APIRouter(prefix="/curves", tags=["Curves"])

@router.get("/{market}")
async def get_curve(market: str):
    return await build_curve(market)
