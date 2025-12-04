import pytest
from unittest.mock import AsyncMock
from app.storage.alsi_client import fetch_alsi_timeseries
import app.storage.alsi_client as http_mod
from tests.conftest import FakeResponse


@pytest.mark.asyncio
async def test_fetch_alsi_timeseries(monkeypatch):

    fake_page = {
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
        return FakeResponse(fake_page)

    monkeypatch.setattr(http_mod, "safe_get", fake_safe_get)

    df = await fetch_alsi_timeseries("EU")

    # Assertions
    assert len(df) == 1
    assert df.iloc[0]["lng_storage_gwh"] == 400
    assert df.iloc[0]["sendOut"] == 22
    assert df.iloc[0]["dtmi_gwh"] == 10
