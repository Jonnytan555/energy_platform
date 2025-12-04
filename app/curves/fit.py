import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline


def fit_monthly_curve(df):
    """
    Fit a cubic spline to a monthly forward curve.
    Produces a smooth curve used for:
        - Netbacks
        - Spread modelling
        - Vol curves
        - Risk
    """

    df = df.sort_values("month").reset_index(drop=True)

    x = np.arange(len(df))
    y = df["price"].values

    spline = CubicSpline(x, y, bc_type="natural")

    xs = np.linspace(0, len(df) - 1, len(df) * 4)
    ys = spline(xs)

    fitted = pd.DataFrame({
        "month": pd.date_range(df["month"].iloc[0], periods=len(xs), freq="7D"),
        "price": ys
    })

    return fitted
