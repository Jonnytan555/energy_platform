import pandas as pd
from app.utils.http import safe_get
from app.config import settings
from app.utils.cache import async_ttl_cache

BASE_URL = "https://alsi.gie.eu/api/data"

@async_ttl_cache(ttl=3600, max_size=32)
async def fetch_alsi_timeseries(country: str = "EU") -> pd.DataFrame:
    headers = {"x-key": settings.ALSI_API_KEY}
    params = {"size": 500}

    if country.upper() == "EU":
        params["type"] = "eu"
    else:
        params["country"] = country.lower()

    all_rows = []
    page = 1

    while True:
        params["page"] = page

        response = await safe_get(BASE_URL, headers=headers, params=params)
        js = response.json()

        rows = js.get("data", [])
        if not rows:
            break

        all_rows.extend(rows)

        if page >= js.get("last_page", 1):
            break

        page += 1

    df = pd.DataFrame(all_rows)
    return _transform(df)


def _transform(df: pd.DataFrame) -> pd.DataFrame:

    # Fix date column
    df["date"] = pd.to_datetime(df["gasDayStart"], errors="coerce")

    # Flatten nested fields
    if "inventory" in df.columns:
        df["lng_storage_gwh"] = pd.to_numeric(df["inventory"].apply(lambda x: x.get("gwh")), errors="coerce")

    if "dtmi" in df.columns:
        df["dtmi_gwh"] = pd.to_numeric(df["dtmi"].apply(lambda x: x.get("gwh")), errors="coerce")

    # Convert simple numeric fields
    numeric_cols = [
        "sendOut",
        "dtrs",
        "contractedCapacity",
        "availableCapacity",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort timeseries
    df = df.sort_values("date")

    df = df.fillna("").replace("", None)

    return df[[
        "date",
        "lng_storage_gwh",
        "sendOut",
        "dtmi_gwh",
        "dtrs",
        "contractedCapacity",
        "availableCapacity",
    ]]
