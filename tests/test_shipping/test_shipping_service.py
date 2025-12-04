import pytest
import asyncio
from app.shipping.ais_service import estimate_eta


@pytest.mark.asyncio
async def test_shipping_service_eta():
    res = await estimate_eta(
        vessel_class="QFlex",
        origin="Ras Laffan",
        destination="Isle of Grain",
        lat=25,
        lon=51,
        speed=14.0,
        timestamp="2025-01-01T12:00:00",
    )

    assert "eta" in res
    assert res["vessel_class"] == "QFlex"
