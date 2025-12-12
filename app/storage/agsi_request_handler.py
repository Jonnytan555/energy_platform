from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from fastapi import HTTPException

from app.config import settings
from app.utils.http import safe_get
from app.utils.cache import async_ttl_cache

logger = logging.getLogger(__name__)

# AGSI base API endpoint: always /api with query params
# Docs example: https://agsi.gie.eu/api?type=eu
BASE_URL = "https://agsi.gie.eu/api"

# Toggle cache easily
USE_CACHE = True


def maybe_cache(func):
    if USE_CACHE:
        return async_ttl_cache(ttl=3600, max_size=32)(func)
    return func


def _build_params(zone: str, page: int) -> dict[str, Any]:
    """
    Build query params for AGSI API.

    - EU aggregate → type=eu
    - Country codes (de, fr, it, ...) → country={zone}
    - Add pagination params (page, size)
    """
    z = zone.lower()

    params: dict[str, Any] = {
        "page": page,
        "size": 300,  # max page size per docs
    }

    if z == "eu":
        params["type"] = "eu"
    else:
        # treat anything else as a country code (de, fr, it, ...)
        params["country"] = z

    return params


def _build_headers() -> dict[str, str]:
    """
    Build headers including AGSI API key.

    Docs: request must include header "x-key: YOUR_API_KEY".
    """
    api_key = settings.API_KEY  # make sure this exists in your settings/env

    if not api_key:
        logger.warning("API_KEY is not set – AGSI will return no data.")
        return {}

    return {"x-key": api_key}


@maybe_cache
async def _fetch_agsi_timeseries(
    zone: str,
    *,
    allow_fallback: bool = True,
    pages_to_fetch: int | None = None
) -> pd.DataFrame:

    headers = _build_headers()

    # First: hit page=1 to discover last_page
    first_params = _build_params(zone, 1)
    first_resp = await safe_get(BASE_URL, headers=headers, params=first_params)
    first_json = first_resp.json()

    last_page = first_json.get("last_page", 1)
    logger.info("AGSI zone=%s discovered last_page=%s", zone, last_page)

    # Determine page window
    if pages_to_fetch is not None:
        start_page = max(1, last_page - pages_to_fetch + 1)
    else:
        start_page = 1

    logger.info(
        "AGSI fetching pages %s → %s (latest %s pages)",
        start_page, last_page, pages_to_fetch
    )

    pages: list[dict] = []

    # Fetch only selected pages
    for page in range(start_page, last_page + 1):

        params = _build_params(zone, page)
        resp = await safe_get(BASE_URL, headers=headers, params=params)
        json_data = resp.json()

        data = json_data.get("data") or []
        logger.info(
            "AGSI page=%s items=%s (partial fetch)",
            page, len(data)
        )

        if not data:
            if not pages:
                if not allow_fallback:
                    raise HTTPException(
                        status_code=502,
                        detail=f"No AGSI data available for zone={zone}"
                    )
                return pd.DataFrame()
            break

        pages.extend(data)

    if not pages:
        return pd.DataFrame()

    df = pd.DataFrame(pages)

    if "gas_day" in df.columns:
        df["gas_day"] = pd.to_datetime(df["gas_day"], errors="coerce")
        df = df.sort_values("gas_day").reset_index(drop=True)

    return df



class AgsiRequestHandler:
    def __init__(self, zone: str, *, allow_fallback: bool = True) -> None:
        self.zone = zone
        self.allow_fallback = allow_fallback

    async def handle_async(self, *, pages_to_fetch: int | None = None) -> pd.DataFrame:
        df = await _fetch_agsi_timeseries(
            self.zone,
            allow_fallback=self.allow_fallback,
            pages_to_fetch=pages_to_fetch,
        )
        logger.info("AGSI handler: zone=%s rows=%s", self.zone, len(df))
        return df
