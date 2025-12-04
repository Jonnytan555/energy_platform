from fastapi import APIRouter

from app.shipping.ais_service import estimate_eta
from .shipping_service import get_shipping_status

router = APIRouter(prefix="/shipping", tags=["Shipping"])


@router.get("/eta")
async def get_eta(
    vessel_class: str = "QFlex",
    origin: str = "Ras Laffan",
    destination: str = "Isle of Grain",
    lat: float = 25.3,
    lon: float = 52.9,
    speed: float = 15.0,
    timestamp: str = "2025-01-01T12:00:00",
):
    """
    AIS-based ETA model combining:
    - vessel physics
    - weather slowdown
    - routing distances
    - congestion delays
    - boiloff estimation
    """

    return await estimate_eta(
        vessel_class=vessel_class,
        origin=origin,
        destination=destination,
        lat=lat,
        lon=lon,
        speed=speed,
        timestamp=timestamp,
    )
