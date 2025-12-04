import pandas as pd
from app.curves.expand import expand_strips_to_months

def test_expand_strips_to_months():
    df = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=40, freq="D"),
        "price": range(40)
    })

    out = expand_strips_to_months(df)
    assert "month" in out.columns
    assert "price" in out.columns
    assert len(out) >= 1
