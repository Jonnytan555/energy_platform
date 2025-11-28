from fastapi import APIRouter
from .curve_builder import build_ttf_curve

router = APIRouter(prefix="/curves", tags=["Curves"])


@router.post("/ttf")
async def ttf_curve(strip: dict):
    """
    Body example:
    {
      "2025-01": 33.1,
      "2025-02": 34.4,
      "2025-03": 35.0
    }
    """
    df = build_ttf_curve(strip)
    return df.to_dicts()

