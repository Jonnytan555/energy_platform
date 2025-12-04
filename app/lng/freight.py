# app/lng/freight.py

ROUTE_DISTANCES_NM = {
    ("USGC", "EU"): 4300,
    ("USGC", "UK"): 4100,
    ("USGC", "NE"): 4400,
    ("USGC", "JP"): 9300,
    ("QA", "EU"): 6200,
}


def freight_cost_usd_per_mmbtu(
    route: tuple,
    charter_rate_usd_day: float = 75000,
    fuel_cost_usd_ton: float = 900,
    vessel_speed_knots: float = 14,
    fuel_consumption_tpd: float = 110,
    cargo_mmbtu: float = 170_000 * 52,  # 170k m3 @ 52 MMBtu per m3 LNG
):
    """
    Compute freight cost in USD per delivered MMBtu.
    """

    if route not in ROUTE_DISTANCES_NM:
        raise ValueError(f"Unknown route {route}")

    distance_nm = ROUTE_DISTANCES_NM[route]

    voyage_days = distance_nm / (vessel_speed_knots * 24)

    # Total cost
    charter_cost = charter_rate_usd_day * voyage_days
    fuel_cost = fuel_cost_usd_ton * (fuel_consumption_tpd * voyage_days)

    total_cost = charter_cost + fuel_cost

    return total_cost / cargo_mmbtu
