from fastapi import HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jwt.exceptions import InvalidTokenError
import jwt

from app.models import User
from app.schemas import TokenPayload
from app.core.config import settings
from app.core import security
from app.core.database import SessionDep

from typing import Annotated
from datetime import datetime

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/access-token')

# TokenDep = Annotated[str, Depends(oauth2_scheme)]

# async def get_current_user(db: SessionDep, token: TokenDep) -> User:
#     # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
#     # token_data = TokenPayload(**payload)
#     # return await db.get(User, token_data.sub)
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
#         token_data = TokenPayload(**payload)
#         if token_data.exp < datetime.utcnow().timestamp():
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token has expired",
#             )
#         print(type(token_data.sub)) # int 
#     except (InvalidTokenError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     db_user = await db.get(User, int(token_data.sub))
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user




async def get_current_user(db: SessionDep, request: Request) -> User:
    token = request.cookies.get("access_token")

    print(f"Received token: {token}")  # Выводим токен в консоль    

    #Raise error if token isn't received
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
        )

    #try to get data from token 
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
        #converts to TokenPayload form sub and exp

        # check for expired time of life 
        if token_data.exp < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
    #if got errors while decoding raise error
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials!"
        )

    #if token was encoded, get an user from DB PG in my case
    db_user = await db.get(User, int(token_data.sub))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not fould in token processing!")
    
    return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]


# async def get_current_user(db: SessionDep, token: TokenDep) -> User:
    # try:
    #     payload = jwt.decode(token, settings.SECRET_KEY, security.ALGORITHM)
    #     token_data = TokenPayload(**payload)

    #     if token_data.sub is None:
    #         raise credentials_exception
        

    # except (InvalidTokenError, ValueError):
    #     raise credentials_exception
    
    # db_user = await db.get(User, token_data.sub)
    # if not db_user:
    #     raise HTTPException(status_code=404, detail="User not found")
    # return db_user