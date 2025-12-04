from fastapi import APIRouter
from ..market.futures_service import get_futures_snapshot

router = APIRouter()

@router.get("/")
async def futures():
    return await get_futures_snapshot()
