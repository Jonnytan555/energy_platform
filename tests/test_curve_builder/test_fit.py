import pandas as pd
from app.curves.fit import fit_monthly_curve

def test_fit_monthly_curve():
    df = pd.DataFrame({
        "month": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01"]),
        "price": [10, 20, 30]
    })

    out = fit_monthly_curve(df)

    assert "price" in out.columns
    assert len(out) > 3   # spline expands data
