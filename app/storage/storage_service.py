from .eia_client import fetch_eia_storage
from .agsi_client import fetch_agsi_storage


class StorageService:

    def __init__(self, eia_key: str, agsi_key: str):
        self.eia_key = eia_key
        self.agsi_key = agsi_key

    async def get_eia(self, weeks: int = 20):
        df = await fetch_eia_storage(self.eia_key, weeks=weeks)
        return df.to_dicts()

    async def get_agsi(self, country: str = "EU"):
        df = await fetch_agsi_storage(self.agsi_key, country=country)
        return df.to_dicts()

