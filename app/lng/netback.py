# app/lng/netback.py

import pandas as pd
from app.curves.builder import build_curve
from .freight import freight_cost_usd_per_mmbtu
from .boiloff import boiloff_loss_mmbtu
from .routing import get_voyage_days


def compute_netback(jkm: float, freight: float, losses_pct: float = 0.07):
    """
    Simple LNG netback formula:
    Netback = JKM - freight - (JKM * losses_pct)
    """
    return jkm - freight - (jkm * losses_pct)


async def build_netback_curve(
    origin="USGC",
    destination="EU",
    market="JKM",
    charter_rate=75000,
    fuel_cost=900,
):
    """
    Computes full monthly LNG netback curve.
    """

    # Step 1 — Fetch monthly price curve
    curve = await build_curve(market)
    df = pd.DataFrame(curve["monthly"])

    # Step 2 — Freight USD/MMBtu
    fc = freight_cost_usd_per_mmbtu(
        (origin, destination),
        charter_rate_usd_day=charter_rate,
        fuel_cost_usd_ton=fuel_cost,
    )

    # Step 3 — Boiloff loss in USD/MMBtu
    days = get_voyage_days(origin, destination)
    bor_loss_mmbtu = boiloff_loss_mmbtu(days)
    bor_loss_usd_mmbtu = bor_loss_mmbtu / (170_000 * 52)

    # Step 4 — Netback per month
    df["netback"] = df["price"] - fc - bor_loss_usd_mmbtu

    return {
        "origin": origin,
        "destination": destination,
        "freight_usd_mmbtu": fc,
        "bor_loss_usd_mmbtu": bor_loss_usd_mmbtu,
        "netback_curve": df.to_dict(orient="records"),
    }
