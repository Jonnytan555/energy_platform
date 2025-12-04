import pytest
from unittest.mock import AsyncMock, patch
from app.curves.builder import build_curve
import pandas as pd

@pytest.mark.asyncio
async def test_build_curve_structure(monkeypatch):
    months = pd.date_range("2025-01-01", periods=12, freq="MS")
    fake_df = pd.DataFrame({
        "date": months,
        "price": list(range(12)),
    })

    monkeypatch.setattr(
        "app.curves.builder.load_market_futures",
        AsyncMock(return_value=fake_df)
    )

    result = await build_curve("TTF")

    assert "market" in result
    assert "raw" in result
    assert "monthly" in result
    assert "daily" in result


