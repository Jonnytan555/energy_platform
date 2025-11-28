from fastapi import APIRouter, Depends
from .storage_service import StorageService

def get_storage_service():
    # Replace with your secrets source
    return StorageService(
        eia_key="YOUR_EIA_KEY",
        agsi_key="YOUR_AGSI_KEY"
    )

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.get("/eia")
async def _get_eia(
    weeks: int = 20,
    svc: StorageService = Depends(get_storage_service)
):
    """
    U.S. EIA Weekly Gas Storage.
    Returns: [{date, storage_bcf}, ...]
    """
    return await svc.get_eia(weeks)


@router.get("/agsi")
async def _get_agsi(
    country: str = "EU",
    svc: StorageService = Depends(get_storage_service)
):
    """
    European AGSI+ Gas Storage.
    Returns: [{date, full_pct, working_gas_gwh, injection, withdrawal}]
    """
    return await svc.get_agsi(country)

