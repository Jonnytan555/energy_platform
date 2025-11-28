from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token

