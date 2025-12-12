import pandas as pd
from pathlib import Path

def load_parquet_fallback() -> pd.DataFrame:
    """
    Fallback loader for AGSI timeseries.
    Used ONLY when AGSI API returns no data AND allow_fallback=True.

    In tests, allow_fallback=False prevents this from running.
    If no fallback file exists, return an empty DataFrame.
    """

    # Example expected path: app/storage/data/agsi_fallback.parquet
    fallback_path = Path(__file__).resolve().parent / "data" / "agsi_fallback.parquet"

    # If no file exists → return empty (safe behaviour for production & tests)
    if not fallback_path.exists():
        return pd.DataFrame()

    try:
        return pd.read_parquet(fallback_path)
    except Exception:
        # Corrupt or unreadable → still fail safe
        return pd.DataFrame()
