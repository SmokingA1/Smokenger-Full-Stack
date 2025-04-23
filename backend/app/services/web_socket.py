from app.services.user import get_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

from fastapi import HTTPException,status
import jwt
from app.schemas import TokenPayload
from app.core.config import settings
from app.core import security
from datetime import datetime
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

async def get_current_user_ws(token: str, db: AsyncSession) -> User:
    print(f"Received token: {token}")  # Выводим токен в консоль    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)

        if token_data.exp < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials!"
        )

    db_user = await db.get(User, int(token_data.sub))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not fould in token processing!")
    
    return db_user