import pandas as pd

from scraper.response.response_handler import ResponseHandler


class AlsiResponseHandler(ResponseHandler):
    """
    Takes the raw ALSI DataFrame from AlsiRequestHandler and:
      - normalises dates
      - flattens nested inventory/dtmi objects
      - casts numerics
      - returns a clean, analytics-ready DataFrame
    """

    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame()

        # --- Date column --- #
        df["date"] = pd.to_datetime(df["gasDayStart"], errors="coerce")

        # --- Flatten nested JSON fields --- #
        if "inventory" in df.columns:
            df["lng_storage_gwh"] = pd.to_numeric(
                df["inventory"].apply(lambda x: x.get("gwh") if isinstance(x, dict) else None),
                errors="coerce",
            )

        if "dtmi" in df.columns:
            df["dtmi_gwh"] = pd.to_numeric(
                df["dtmi"].apply(lambda x: x.get("gwh") if isinstance(x, dict) else None),
                errors="coerce",
            )

        # --- Simple numeric fields --- #
        numeric_cols = [
            "sendOut",
            "dtrs",
            "contractedCapacity",
            "availableCapacity",
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Sort timeseries
        df = df.sort_values("date")

        # Normalise nulls
        df = df.fillna("").replace("", None)

        # Final column order (same as your original _transform)
        return df[
            [
                "date",
                "lng_storage_gwh",
                "sendOut",
                "dtmi_gwh",
                "dtrs",
                "contractedCapacity",
                "availableCapacity",
            ]
        ]
