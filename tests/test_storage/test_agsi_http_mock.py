import pytest
import app.utils.http as http_mod

from unittest.mock import AsyncMock
from app.storage.agsi_client import fetch_agsi_timeseries

@pytest.mark.asyncio
async def test_agsi_http_layer(monkeypatch):
    class FakeResponse:
        def json(self):
            return {"data": [], "last_page": 1}

    monkeypatch.setattr(
        "app.utils.http.safe_get",
        AsyncMock(return_value=FakeResponse())
    )

    df = await fetch_agsi_timeseries("EU")
    assert df.empty

