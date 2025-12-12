import asyncio
import pandas as pd

from typing import Any, Dict, List
from app.utils.http import safe_get
from app.utils.cache import async_ttl_cache
from app.config import settings
from scraper.request.request_handler import RequestHandler

BASE_URL = "https://alsi.gie.eu/api/data"


class AlsiRequestHandler(RequestHandler):
    """
    RequestHandler implementation that fetches raw ALSI data
    (list of dicts / JSON) from the ALSI API.
    """

    def __init__(self, country: str = "EU", allow_fallback: bool = True):
        self.country = country
        self.allow_fallback = allow_fallback

    async def handle_async(self) -> pd.DataFrame:
        return await _fetch_alsi_timeseries(
            country=self.country,
            allow_fallback=self.allow_fallback,
        )

    def handle(self) -> pd.DataFrame:
        return asyncio.run(self.handle_async())


@async_ttl_cache(ttl=3600, max_size=32)
async def _fetch_alsi_timeseries(
    country: str = "EU",
    *,
    allow_fallback: bool = True,
) -> pd.DataFrame:
    """
    Low-level ALSI fetcher.

    - Reads ALSI_API_KEY from settings
    - Paginates ALSI API
    - Returns *raw* DataFrame (no column renames / numeric casts)
    """

    headers = {"x-key": settings.API_KEY}
    params: Dict[str, Any] = {"size": 500}

    if country.upper() == "EU":
        params["type"] = "eu"
    else:
        params["country"] = country.lower()

    all_rows: List[Dict[str, Any]] = []
    page = 1

    while True:
        params["page"] = page

        resp = await safe_get(BASE_URL, headers=headers, params=params)
        js = resp.json()

        rows = js.get("data", [])
        if not rows:
            # In tests you might set allow_fallback=False and assert empty
            if not allow_fallback:
                return pd.DataFrame()
            break

        all_rows.extend(rows)

        if page >= js.get("last_page", 1):
            break

        page += 1

    df = pd.DataFrame(all_rows)

    # No fallback parquet for ALSI here (you can add if you want)
    return df
