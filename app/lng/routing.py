# app/lng/routing.py

ROUTE_DAYS = {
    ("USGC", "EU"): 12.5,
    ("USGC", "UK"): 11.8,
    ("USGC", "NE"): 13.2,
    ("QA", "EU"): 17.5,
    ("QA", "UK"): 16.8,
    ("QA", "JP"): 13.0,
}


def get_voyage_days(origin: str, destination: str) -> float:
    key = (origin, destination)
    if key not in ROUTE_DAYS:
        raise ValueError(f"Unknown voyage route {origin}->{destination}")
    return ROUTE_DAYS[key]


def compute_route(origin: str, destination: str):
    return {
        "origin": origin,
        "destination": destination,
        "voyage_days": get_voyage_days(origin, destination),
    }
