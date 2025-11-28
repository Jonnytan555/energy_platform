import httpx
import polars as pl


BASE_URL = "https://agsi.gie.eu/api"


async def fetch_agsi_storage(api_key: str, country: str = "EU") -> pl.DataFrame:
    """
    AGSI+ European gas storage feed.
    Country example: DE, FR, IT, ES, EU (aggregate)
    """

    headers = {"x-key": api_key}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BASE_URL}/stocks/{country}", headers=headers)
        r.raise_for_status()
        raw = r.json()["data"]

    df = pl.DataFrame(raw)

    return (
        df
        .select([
            pl.col("gasDayStart").str.strptime(pl.Date, "%Y-%m-%d"),
            pl.col("full"),
            pl.col("injection").cast(pl.Float64),
            pl.col("withdrawal").cast(pl.Float64),
            pl.col("workingGasVolume").cast(pl.Float64),
        ])
        .rename({
            "gasDayStart": "date",
            "full": "full_pct",
            "workingGasVolume": "working_gas_gwh"
        })
        .sort("date")
    )

