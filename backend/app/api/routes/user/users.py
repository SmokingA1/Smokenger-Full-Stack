from fastapi import APIRouter, HTTPException, Depends, Path, Query
from sqlalchemy.future import select
from app.core.database import SessionDep
from app.models import User
from app.schemas import (
    UserRegister,
    UserPublic,
    UserUpdate,
    UserUpdateMe, 
    UserUpdatePassword,
    UserUpdateName,
    Message)
from app.services.user import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_phone,
    update_user,
    update_user_me,
    update_user_me_name,
    get_users, 
    create_user,
    delete_user,
)
from app.api.deps import CurrentUser
from app.core.security import verify_password, hash_password
from typing import Annotated, List, Any

router = APIRouter(prefix='/users', tags=['Users'])

@router.get("/email", response_model=UserPublic)
async def read_user_with_email(
    db: SessionDep,
    user_email: str = Query(..., title='The email is required!')
):
    if not user_email:
        raise HTTPException(status_code=400, detail='Email is required!')
        
    db_user = await get_user_by_email(db, user_email)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found!')
    return db_user


@router.get('/me', response_model=UserPublic)
async def read_user_me(current_user: CurrentUser):
    return current_user


@router.get("/phone", response_model=UserPublic)
async def read_user(db: SessionDep, user_phone: str = Query(..., title="The phone is required!")) -> Any:
    db_user = await get_user_by_phone(db, user_phone)
    if not db_user: 
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user


@router.get("/", response_model=List[UserPublic])
async def read_users(
    db: SessionDep,
    page: int = Query(1, title="The number of page is required!"),
    limit: int = Query(20, title="The quantity of users is required!")
) -> Any:
    db_users = await get_users(db, page, limit)
    if not db_users:
        raise HTTPException(status_code=404, detail='Users not found!')
    return db_users


@router.post('/signup', response_model=Message)
async def register_user(
    db: SessionDep,
    user_create: UserRegister,
) -> Any:
    """
    Register new user
    """
    db_email = await get_user_by_email(db, user_create.email)
    if db_email:
        raise HTTPException(status_code=409, detail='Such email already exists.')
    db_phone = await get_user_by_phone(db, user_create.phone_number)
    if db_phone:
        raise HTTPException(status_code=409, detail='Such phone number already exists.')
    new_user = await create_user(db, user_create)
    if not new_user:
        raise HTTPException(status_code=400, detail='Something went wrong, try again later!')
    
    return Message(data="User was registered successfully!")


@router.get('/{id}', response_model=UserPublic)
async def read_user_by_id(db: SessionDep, id: int):
    db_user = await get_user_by_id(db, id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found!')
    return db_user


@router.put('/update/{user_id}', response_model=UserPublic)
async def update_user_by_id(db: SessionDep, user_id: int, user_update: UserUpdate):
    """
    Update user by id
    """
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found!')
    
    if user_update.email:
        existing_user = await get_user_by_email(db, user_email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=404, detail='Such email already exists!')
    
    if user_update.phone_number:
        db_phone = await get_user_by_phone(db, user_update.phone_number)
        if db_phone and db_phone.id != user_id:
            raise HTTPException(status_code=404, detail='Such phone number already exists.')
    
    if user_update.password:
        if verify_password(user_update.password,  db_user.hashed_password):
            raise HTTPException(status_code=400, detail='Password cannot be same as current one.')
        
    updated_user = await update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail='Incorrect data!')
    return updated_user


@router.put("/me/update/name", response_model=Message)
async def update_my_user_name(db: SessionDep, current_user: CurrentUser, user_updaet_name: UserUpdateName):
    updated_user = await update_user_me_name(db, current_user.id, user_updaet_name.new_name)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    return Message(data="User updated successfully!")
    


@router.delete("/delete/{user_id}", response_model=Message)
async def delete_user_by_id(db: SessionDep, user_id:int) -> Any:
    """Delete an user by id"""
    deleted_user = await delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail='User not found!')
    return Message(data='User deleted successfully!')
    

@router.put('/me/update', response_model=UserPublic)
async def update_my_user(db: SessionDep, current_user: CurrentUser, user_update: UserUpdateMe):
    """
    Update own user
    """
    if user_update.email:
        db_user = await get_user_by_email(db, user_email=user_update.email)
        if db_user and db_user.id != current_user.id:
            raise HTTPException(status_code=404, detail='Such email already exists1')
    updated_user = await update_user_me(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail='Incorrect data!')
    return updated_user

@router.put('/me/update-password', response_model=Message)
async def update_my_password(
    db: SessionDep,
    current_user: CurrentUser,
    passwords: UserUpdatePassword
) -> Any:
    """
    Update logged in user's password.
    """
    if not verify_password(passwords.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect password')
    if passwords.new_password == passwords.current_password:
        raise HTTPException(status_code=400, detail='New password cannot be the same as the current one!')
    new_hashed_password = hash_password(passwords.new_password)
    current_user.hashed_password = new_hashed_password
    await db.commit()
    await db.refresh(current_user)
    return Message(data='Password updated successfully!')

@router.delete('/me/delete', response_model=Message)
async def delete_my_user(
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Delete own user.
    """
    deleted_user = await delete_user(db, current_user.id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found!")
    return Message(data='User deleted successfully')
