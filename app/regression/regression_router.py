from fastapi import APIRouter
from .regression_service import run_regression

router = APIRouter()

@router.get("/")
async def regression():
    return await run_regression()
