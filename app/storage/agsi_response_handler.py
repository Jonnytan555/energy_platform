import logging
import pandas as pd
from scraper.response.response_handler import ResponseHandler


class AgsiResponseHandler(ResponseHandler):
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans and normalises AGSI timeseries output.

        Accepts:
        - raw AGSI schema with 'gasDayStart', or
        - pre-normalised schema with 'date'.

        If the frame is empty or has no recognised columns, it returns an
        empty frame instead of raising, so the API response is just [].
        """

        # --- handle empty / missing data safely ---------------------
        if df is None or df.empty or not len(df.columns):
            logging.warning("AGSI response handler received empty DataFrame.")
            # return a well-shaped but empty frame
            return pd.DataFrame(
                columns=[
                    "date",
                    "gas_in_storage_gwh",
                    "injection",
                    "withdrawal",
                    "working_gas_gwh",
                    "full_pct",
                    "trend",
                ]
            )

        cols = set(df.columns)

        # --- ensure we have a 'date' column -------------------------
        if "gasDayStart" in cols:
            # raw AGSI payload
            df["date"] = pd.to_datetime(df["gasDayStart"], errors="coerce")
        elif "date" in cols:
            # already normalised (e.g. parquet fallback / earlier transform)
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        else:
            logging.warning(
                "AGSI response handler expected 'gasDayStart' or 'date', "
                f"got columns: {sorted(cols)}. Returning data unchanged."
            )
            return df

        # --- rename columns to pythonic names -----------------------
        df = df.rename(
            columns={
                "gasInStorage": "gas_in_storage_gwh",
                "workingGasVolume": "working_gas_gwh",
                "full": "full_pct",
            }
        )

        # --- numeric cleaning ---------------------------------------
        numeric_cols = [
            "gas_in_storage_gwh",
            "injection",
            "withdrawal",
            "working_gas_gwh",
            "full_pct",
            "trend",
        ]

        for c in numeric_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")

        # --- sort & tidy --------------------------------------------
        df = df.sort_values("date")
        df = df.fillna("").replace("", None)

        desired_cols = [
            "date",
            "gas_in_storage_gwh",
            "injection",
            "withdrawal",
            "working_gas_gwh",
            "full_pct",
            "trend",
        ]
        existing = [c for c in desired_cols if c in df.columns]

        return df[existing]
