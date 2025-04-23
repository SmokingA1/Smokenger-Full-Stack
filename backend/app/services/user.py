from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import (
    UserCreate,
    UserUpdate,
    UserUpdateMe,
    UserUpdatePassword
)
from sqlalchemy.future import select
from typing import List, Any
from app.core.security import hash_password, verify_password

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    db_user = await db.get(User, user_id)
    return db_user

async def get_user_by_email(db: AsyncSession, user_email: str) -> User:
    db_user = await db.execute(select(User).where(User.email == user_email))
    return db_user.scalars().first()

async def get_user_by_phone(db: AsyncSession, user_phone: str) -> User:
    db_user = await db.execute(select(User).where(User.phone_number == user_phone))
    return db_user.scalars().first()

async def get_users(db: AsyncSession, page: int = 1, limit: int = 20) -> List[User]:
    query = select(User)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    db_users = await db.execute(query)
    
    return db_users.scalars().all()

async def create_user(db: AsyncSession, user_create: UserCreate) -> User:    
    print(user_create)

    new_user = User(full_name = user_create.full_name,
                    hashed_password = hash_password(user_create.password),
                    email = user_create.email,
                    phone_number = user_create.phone_number
                    )   
                    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    if 'password' in update_data:
        new_password = hash_password(update_data['password'])
        db_user.hashed_password = new_password
        

    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user_me(db: AsyncSession, user_id, user_update: UserUpdateMe) -> Any:
    db_user = await get_user_by_id(db, user_id)

    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user_me_name(db: AsyncSession, user_id: int, new_name: str) -> Any:
    db_user = await get_user_by_id(db, user_id)
    print('HERERERERERERER')
    if not db_user:
        return None
    
    db_user.full_name = new_name
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    return db_user

async def authenticate(db: AsyncSession, email: str, password: str) -> User:
    db_user = await get_user_by_email(db, user_email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user