import httpx
import polars as pl
from datetime import datetime, timedelta


BASE_URL = "https://api.eia.gov/v2/natural-gas/stor/wngsr/data/"


async def fetch_eia_storage(api_key: str, weeks: int = 12) -> pl.DataFrame:
    """
    Fetch weekly U.S. gas storage (EIA WNGSR).
    """
    end = datetime.utcnow().date()
    start = end - timedelta(weeks=weeks)

    params = {
        "api_key": api_key,
        "frequency": "weekly",
        "data[0]": "value",
        "start": str(start),
        "end": str(end),
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()
        raw = r.json()["response"]["data"]

    df = pl.DataFrame(raw)

    return (
        df
        .select([
            pl.col("period").str.strptime(pl.Date, "%Y-%m-%d"),
            pl.col("value").cast(pl.Float64)
        ])
        .rename({"period": "date", "value": "storage_bcf"})
        .sort("date")
    )

