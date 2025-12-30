import asyncio
import httpx

from retry import retry


# ---------------------------------------
# Shared async HTTP GET with retries
# ---------------------------------------
@retry(
    exceptions=(httpx.ReadTimeout, httpx.HTTPStatusError),
    tries=5,
    delay=1,
    backoff=2,
)
async def safe_get(url: str, *, headers=None, params=None, timeout=30):
    """
    Shared safe async GET request with retry logic.
    Used by AGSI + ALSI + curves + weather + anything needing HTTP.
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, params=params, timeout=timeout)
        r.raise_for_status()
        return r
    

# ---------------------------------------
# Run async from sync
# ---------------------------------------
def run_sync(async_fn, *args, **kwargs):
    """
    Runs any async function from synchronous code.
    Example:
        df = run_sync(fetch_agsi_timeseries, "EU")
    """
    return asyncio.run(async_fn(*args, **kwargs))
