from app.storage.agsi_client import fetch_agsi_timeseries
from app.config import settings
from app.storage.asli_client import fetch_alsi_timeseries


class StorageService:
    
    async def get_agsi(self):
        """
        Return AGSI EU gas-storage timeseries (via AGSI API).
        """
        df = await fetch_agsi_timeseries(
            country="EU"
        )
        return df.Dataframe.to_dicts()
    
    async def get_asli(self):
        """
        Return AGSI EU gas-storage timeseries (via AGSI API).
        """
        df = await fetch_alsi_timeseries(
            country="EU"
        )
        return df.Dataframe.to_dicts()
