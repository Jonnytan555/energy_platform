import polars as pl
import numpy as np
from datetime import date
from scipy.interpolate import CubicSpline


def build_ttf_curve(strip: dict) -> pl.DataFrame:
    """
    Convert monthly forward strip to daily smooth curve.
    strip = {"2025-01": 33.5, "2025-02": 34.7, ...}
    """

    # Convert strip → polars
    df = pl.DataFrame({
        "month": list(strip.keys()),
        "price": list(strip.values())
    }).with_columns([
        pl.col("month").str.strptime(pl.Date, "%Y-%m"),
    ])

    # Build numeric x-values
    df = df.sort("month").with_columns([
        pl.col("month").cast(pl.Datetime).dt.timestamp().alias("ts")
    ])

    x = df["ts"].to_numpy()
    y = df["price"].to_numpy()

    # Cubic spline
    spline = CubicSpline(x, y)

    # Daily range from first → last month
    start = df["month"].min()
    end = df["month"].max().replace(day=28)  # safe end

    day_range = pl.date_range(start, end, "1d", eager=True)
    ts_interp = (
        day_range.cast(pl.Datetime)
        .dt.timestamp()
        .to_numpy()
    )

    curve = spline(ts_interp)

    return pl.DataFrame({
        "date": day_range,
        "price_interp": curve
    })

