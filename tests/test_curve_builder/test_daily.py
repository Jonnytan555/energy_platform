import pytest
import pandas as pd
from app.curves.daily import interpolate_daily

def test_interpolate_daily():
    
    months = pd.date_range("2025-01-01", periods=12, freq="MS")
    prices = list(range(12))

    df = pd.DataFrame({
        "month": months,
        "price": prices,
    })

    result = interpolate_daily(df)

    assert len(result) == 365
    assert "date" in result.columns
    assert "price" in result.columns


