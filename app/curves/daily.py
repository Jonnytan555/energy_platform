from scipy.interpolate import interp1d
import pandas as pd

def interpolate_daily(df):
    df = df.sort_values(df.columns[0]).reset_index(drop=True)

    # Convert month → integer offsets
    df["t"] = (df[df.columns[0]] - df[df.columns[0]].min()).dt.days

    # Create interpolation function that allows extrapolation
    f = interp1d(
        df["t"],
        df["price"],
        kind="linear",
        bounds_error=False,
        fill_value="extrapolate",
    )

    # Generate 365 days of values starting from day 0
    t_days = pd.RangeIndex(0, 365)
    prices = f(t_days)

    return pd.DataFrame({
        "date": df[df.columns[0]].min() + pd.to_timedelta(t_days, unit="D"),
        "price": prices,
    })
