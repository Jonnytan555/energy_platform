import pandas as pd
from scipy.interpolate import interp1d


def interpolate_daily(df):
    """
    Convert monthly curve → daily forward curve.
    Used by:
        - VAR
        - Greeks
        - Daily risk systems
    """

    monthly = df.copy()
    monthly["t"] = (monthly["month"] - monthly["month"].iloc[0]).dt.days

    f = interp1d(monthly["t"], monthly["price"], kind="linear")

    days = pd.date_range(start=monthly["month"].iloc[0], periods=365, freq="D")
    t_days = (days - days[0]).days

    prices = f(t_days)

    return pd.DataFrame({"date": days, "price": prices})
