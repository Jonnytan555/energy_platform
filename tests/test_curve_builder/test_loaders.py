import pytest
import pandas as pd
from app.curves.loaders import load_market_futures

@pytest.mark.asyncio
async def test_load_market_futures(monkeypatch):

    async def fake_fetch(market, days):
        return pd.DataFrame({
            "date": ["2025-01-01", "2025-01-02"],
            "price": [30.0, 31.0],
        })

    monkeypatch.setattr(
        "app.curves.loaders.fetch_futures", 
        fake_fetch
    )

    df = await load_market_futures("TTF", 10)

    assert len(df) == 2
    assert list(df.columns) == ["date", "price"]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
