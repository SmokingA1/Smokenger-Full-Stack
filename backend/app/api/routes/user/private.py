from fastapi import APIRouter

from app.models import User
from app.core.database import SessionDep
from app.schemas import UserPublic, UserRegister
from app.core.security import hash_password
router = APIRouter(prefix='/private', tags=['Private'])

@router.post('/users/private', response_model=UserPublic)
async def create_private_user(db: SessionDep, user_register: UserRegister):

    new_user = User(
        email = user_register.email,
        hashed_password = hash_password(user_register.password),
        full_name = user_register.full_name
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user