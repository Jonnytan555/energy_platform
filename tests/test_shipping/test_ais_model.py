import pytest
from datetime import datetime
from app.shipping.ais_model import compute_eta


def test_eta_basic():
    result = compute_eta(
        vessel_class="QFlex",
        origin="Ras Laffan",
        destination="Isle of Grain",
        current_speed=15.0,
        reported_at=datetime(2025, 1, 1, 12, 0, 0),
        weather_factor=1.0,
        congestion_delay_hours=0,
    )

    assert "eta" in result
    assert result["distance_nm"] == 6300
    assert result["speed_knots"] == 15.0
    assert result["effective_speed_knots"] == 15.0
    assert result["voyage_days"] > 10
    assert result["boiloff_pct"] > 0
