def validate_curve(df):
    """
    Validate curve for:
      - negative prices
      - unrealistic jumps
      - arbitrage signals (optional)
    """

    if (df["price"] < 0).any():
        raise ValueError("Negative prices detected in curve!")

    pct = df["price"].pct_change().abs()

    if (pct > 0.4).any():
        print("⚠ Warning: Large discontinuity in curve detected.")
