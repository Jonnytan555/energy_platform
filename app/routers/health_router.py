from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health():
    # Keep it cheap and fast (no DB calls here initially)
    return {"status":"ok"}

