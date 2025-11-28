from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    # check if exists
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(email=email, password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "email": user.email}

