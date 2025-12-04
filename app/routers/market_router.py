from fastapi import APIRouter
from ..market.market_service import get_market_snapshot

router = APIRouter()

@router.get("/")
async def market():
    return await get_market_snapshot()
