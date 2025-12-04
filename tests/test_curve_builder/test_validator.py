import pandas as pd
from app.curves.validator import validate_curve

def test_validate_curve_ok():
    df = pd.DataFrame({
        "month": pd.date_range("2025-01", periods=3, freq="MS"),
        "price": [10, 11, 12]
    })
    validate_curve(df)  # Should not raise

def test_validate_curve_negative_price():
    df = pd.DataFrame({
        "month": pd.date_range("2025-01", periods=3, freq="MS"),
        "price": [10, -1, 12]
    })
    try:
        validate_curve(df)
        assert False, "Should fail"
    except ValueError:
        assert True
