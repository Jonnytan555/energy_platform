import asyncio
import pandas as pd
from app.utils.http import safe_get
from app.config import settings
from app.utils.cache import async_ttl_cache

import pandas as pd
from app.utils.http import safe_get
from app.utils.cache import async_ttl_cache

from app.storage.agsi_fallback import load_parquet_fallback


BASE_URL = "https://agsi.gie.eu/api/data"

from pathlib import Path
import pandas as pd
import json
from app.utils.cache import read_cache, write_cache


@async_ttl_cache(ttl=3600, max_size=32)
async def fetch_agsi_timeseries(zone: str, *, allow_fallback: bool = True):
    """
    allow_fallback=False is used ONLY in tests to prevent loading real data.
    """

    # ---- TEST MODE: return empty if patched safe_get returns empty ----
    pages = []
    page = 1

    while True:
        resp = await safe_get(
            f"https://agsi.gie.eu/api/data/{zone}",
            params={"page": page},
        )
        json_data = resp.json()

        if not json_data["data"]:
            # TEST EXPECTATION: return empty df
            if not allow_fallback:
                return pd.DataFrame()

        pages.extend(json_data["data"])

        if page >= json_data["last_page"]:
            break

        page += 1

    df = pd.DataFrame(pages)

    # If still empty → fallback allowed in production only
    if df.empty and allow_fallback:
        return load_parquet_fallback()

    return transform(df)



def _transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and normalises AGSI timeseries output.
    Ensures all numeric fields are floats and dates sorted.
    """

    # convert date
    df["date"] = pd.to_datetime(df["gasDayStart"], errors="coerce")

    # rename columns to pythonic names
    df = df.rename(columns={
        "gasInStorage": "gas_in_storage_gwh",
        "workingGasVolume": "working_gas_gwh",
        "full": "full_pct",
    })

    # numeric cleaning
    numeric_cols = [
        "gas_in_storage_gwh",
        "injection",
        "withdrawal",
        "working_gas_gwh",
        "full_pct",
        "trend",
    ]

    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.sort_values("date")

    df = df.fillna("").replace("", None)

    return df[[
        "date",
        "gas_in_storage_gwh",
        "injection",
        "withdrawal",
        "working_gas_gwh",
        "full_pct",
        "trend",
    ]]
