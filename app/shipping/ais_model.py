import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ---------------------------------
# Vessel physical characteristics
# ---------------------------------
VESSEL_PROFILES = {
    "QFlex": {
        "design_speed": 19.5,     # knots
        "eco_speed": 16.0,
        "fuel_curve": lambda v: 0.0012 * v**3,   # tonnes fuel/hour
        "boiloff_rate": 0.12,     # % per day
    },
    "QMax": {
        "design_speed": 20.5,
        "eco_speed": 17.5,
        "fuel_curve": lambda v: 0.0015 * v**3,
        "boiloff_rate": 0.15,
    },
    "StandardLNG": {
        "design_speed": 19.0,
        "eco_speed": 15.5,
        "fuel_curve": lambda v: 0.0010 * v**3,
        "boiloff_rate": 0.10,
    }
}


# ---------------------------------
# Distance lookup (nm)
# In the real model this will use Google OR a routing API
# ---------------------------------
DISTANCE_MAP = {
    ("Ras Laffan", "Isle of Grain"): 6300,
    ("Ras Laffan", "Zeebrugge"): 6200,
    ("Sabine Pass", "Gate Rotterdam"): 4800,
    ("Sabine Pass", "Barcelona"): 4300,
}


def get_distance(origin: str, destination: str) -> float:
    """Simple distance resolver."""
    return DISTANCE_MAP.get((origin, destination), None)


# ---------------------------------
# ETA core model
# ---------------------------------
def compute_eta(
    vessel_class: str,
    origin: str,
    destination: str,
    current_speed: float,
    reported_at: datetime,
    weather_factor: float = 0.90,
    congestion_delay_hours: float = 8.0,
):
    """
    AIS-based ETA using vessel physics + weather + congestion.

    weather_factor < 1 → slowdown  
    congestion_delay_hours added at destination
    """

    profile = VESSEL_PROFILES.get(vessel_class)
    if profile is None:
        raise ValueError(f"Unknown vessel class: {vessel_class}")

    distance_nm = get_distance(origin, destination)
    if distance_nm is None:
        raise ValueError(f"No routing available for {origin} → {destination}")

    # Weather-adjusted operational speed
    effective_speed = current_speed * weather_factor

    # ETA time (hours)
    travel_hours = distance_nm / max(effective_speed, 1.0)

    # Add congestion
    travel_hours += congestion_delay_hours

    eta = reported_at + timedelta(hours=travel_hours)

    # Boiloff estimation
    days = travel_hours / 24
    boiloff_pct = days * profile["boiloff_rate"]

    return {
        "origin": origin,
        "destination": destination,
        "vessel_class": vessel_class,
        "distance_nm": distance_nm,
        "speed_knots": current_speed,
        "effective_speed_knots": effective_speed,
        "eta": eta.isoformat(),
        "voyage_days": round(days, 2),
        "boiloff_pct": round(boiloff_pct, 3),
    }
