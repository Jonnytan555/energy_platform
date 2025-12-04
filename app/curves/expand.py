import pandas as pd


def expand_strips_to_months(df):
    """
    Convert futures data into a monthly price series.
    Currently:
        - Resamples daily futures into month-start values
    Later:
        - Add Q1/Q2/Summer/Winter/Cal strip rules
    """

    df = df.copy()
    df = df.resample("MS", on="date").last().dropna()
    df = df.reset_index()

    df.columns = ["month", "price"]
    df["month"] = pd.to_datetime(df["month"])

    return df
