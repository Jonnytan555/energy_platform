# app/lng/lng_router.py

from fastapi import APIRouter
from app.lng.netback import compute_netback, build_netback_curve
from app.lng.freight import freight_cost_usd_per_mmbtu
from app.lng.boiloff import boiloff_loss_mmbtu
from app.lng.routing import compute_route, get_voyage_days

router = APIRouter(prefix="/lng", tags=["LNG"])

# -------------------------
# Point netback
# -------------------------
@router.get("/netback/point")
async def netback_point(jkm: float, freight: float, losses_pct: float = 0.07):
    return {"netback": compute_netback(jkm, freight, losses_pct)}

# -------------------------
# Netback curve
# -------------------------
@router.get("/netback/curve")
async def netback_curve(
    origin: str = "USGC",
    destination: str = "EU",
    market: str = "JKM",
    charter_rate: int = 75000,
    fuel_cost: int = 900,
):
    return await build_netback_curve(
        origin=origin,
        destination=destination,
        market=market,
        charter_rate=charter_rate,
        fuel_cost=fuel_cost,
    )

# -------------------------
# Freight cost
# -------------------------
@router.get("/freight")
async def get_freight(
    origin: str = "USGC",
    destination: str = "EU",
    charter_rate: int = 75000,
    fuel_cost: int = 900,
):
    return {
        "freight_usd_mmbtu": freight_cost_usd_per_mmbtu(
            (origin, destination),
            charter_rate_usd_day=charter_rate,
            fuel_cost_usd_ton=fuel_cost,
        )
    }

# -------------------------
# Boiloff
# -------------------------
@router.get("/boiloff")
async def get_boiloff(origin: str, destination: str, daily_bor_pct: float = 0.12):
    days = get_voyage_days(origin, destination)
    return {
        "voyage_days": days,
        "boiloff_mmbtu": boiloff_loss_mmbtu(days, daily_bor_pct),
    }

# -------------------------
# Routing
# -------------------------
@router.get("/route")
async def route(origin: str, destination: str):
    return compute_route(origin, destination)
