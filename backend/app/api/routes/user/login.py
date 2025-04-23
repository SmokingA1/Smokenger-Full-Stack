from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token
from app.services.user import authenticate, get_user_by_email
from app.core.database import SessionDep
from app.utils import generate_password_reset_token, generate_reset_password_email, send_email
from app.schemas import Message, UserPublic
from app.api.deps import CurrentUser

from typing import Annotated
from datetime import timedelta

router = APIRouter(tags=['Login'])

@router.post('/login/access-token', response_model=Message)
async def login_access_token(db: SessionDep, response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    OAuth compatible token login, get an access token for future requests
    """
    user = await authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password!')
    
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.id, expires_delta=expires_delta)

    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=False,
        httponly=False,
        samesite="Lax",

    )

    return Message(data="Logged in successfully!")

@router.post('/login/test-token', response_model=UserPublic)
async def login_test_token(current_user: CurrentUser):
    """
    Test acces token
    """
    return current_user

@router.post('/password-recover{email}', response_model=str)
async def recover_password(db: SessionDep, email: str):
    user = await get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail='User not found!')
    
    password_reset_token = generate_password_reset_token(email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.htlm_content
    )
    return Message(data="Recovery message sent.")   



@router.get("/clear-cookie")
async def logout(response: Response):
    # Сброс куки при выходе
    response.delete_cookie("access_token")
    return Message(data="Successfully logout!")