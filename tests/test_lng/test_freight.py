import pytest
from app.lng.freight import freight_cost_usd_per_mmbtu


def test_freight_cost():

    cost = freight_cost_usd_per_mmbtu(
        route=("USGC", "EU"),
        charter_rate_usd_day=100_000,
        fuel_cost_usd_ton=800
    )

    assert cost > 0
    assert isinstance(cost, float)
