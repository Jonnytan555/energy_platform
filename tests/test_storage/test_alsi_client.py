import pytest
import pandas as pd
from unittest.mock import AsyncMock
import app.utils.http as http_mod
from app.storage.alsi_client import fetch_alsi_timeseries, _transform


# --------------------------------------------------------------------
# Test TRANSFORM LOGIC directly (deterministic & independent of HTTP)
# --------------------------------------------------------------------
def test_alsi_transform_basic():
    df = pd.DataFrame([
        {
            "gasDayStart": "2025-01-01",
            "inventory": {"gwh": "500"},
            "dtmi": {"gwh": "20"},
            "sendOut": "30",
            "dtrs": "15",
            "contractedCapacity": "800",
            "availableCapacity": "700",
        }
    ])

    out = _transform(df)

    # check required columns exist
    assert "date" in out.columns
    assert "lng_storage_gwh" in out.columns
    assert "dtmi_gwh" in out.columns

    # check numeric conversions
    assert out["lng_storage_gwh"].iloc[0] == 500
    assert out["dtmi_gwh"].iloc[0] == 20
    assert out["sendOut"].iloc[0] == 30
    assert out["dtrs"].iloc[0] == 15


# --------------------------------------------------------------------
# Test FULL async ALSI fetch with monkeypatched safe_get
# --------------------------------------------------------------------
@pytest.mark.asyncio
async def test_fetch_alsi_timeseries(monkeypatch):

    page1 = {
        "data": [
            {
                "gasDayStart": "2025-01-01",
                "inventory": {"gwh": "400"},
                "sendOut": "22",
                "dtmi": {"gwh": "10"},
                "dtrs": "5",
                "contractedCapacity": "900",
                "availableCapacity": "850",
            }
        ],
        "last_page": 1,
    }

    async def fake_safe_get(*args, **kwargs):
        class FakeResponse:
            def json(self_inner):
                return page1
        return FakeResponse()

    monkeypatch.setattr(http_mod, "safe_get", fake_safe_get)

    df = await fetch_alsi_timeseries("EU")

    assert not df.empty
    assert len(df) == 1

    assert df["lng_storage_gwh"].iloc[0] == 400
    assert df["dtmi_gwh"].iloc[0] == 10
    assert df["sendOut"].iloc[0] == 22
    assert "availableCapacity" in df.columns
