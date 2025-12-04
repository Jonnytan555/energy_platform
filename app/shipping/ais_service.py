from datetime import datetime
from app.shipping.ais_model import compute_eta


async def estimate_eta(
    vessel_class: str,
    origin: str,
    destination: str,
    lat: float,
    lon: float,
    speed: float,
    timestamp: str,
):
    """
    This simulates an AIS feed.
    Your future real AIS ingestion will slot in here.
    """

    reported_at = datetime.fromisoformat(timestamp)

    result = compute_eta(
        vessel_class=vessel_class,
        origin=origin,
        destination=destination,
        current_speed=speed,
        reported_at=reported_at,
        weather_factor=0.92,            # TODO: hook into weather API
        congestion_delay_hours=6.0      # TODO: dynamic congestion model
    )

    return result
