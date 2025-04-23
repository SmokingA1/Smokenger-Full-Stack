from fastapi import APIRouter, HTTPException, Query, Path
from app.schemas import Message
from app.core.database import SessionDep
from app.schemas import ChatMemberRead, ChatMemberCreate
from app.services.user import get_user_by_id
from app.services.chat.chat import get_chat_by_id
from app.services.chat.member import (
    get_chat_member_by_id,
    get_chat_members,
    create_chat_member,
    create_chat_member_my,
    delete_chat_member,
    delete_chat_member_me,
)

from typing import Any, List, Annotated

from app.api.deps import CurrentUser

router = APIRouter(prefix='/chat-members', tags=['ChatMember'])


@router.get('/{chat_id}/members', response_model=List[ChatMemberRead])
async def read_chat_members(
    db: SessionDep,
    chat_id: Annotated[int, Path(..., title='The chat id is required!')]
) -> Any:
    db_chat = await get_chat_by_id(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail='Chat not found!')
    
    db_chat_members = await get_chat_members(db, chat_id)
    if not db_chat_members:
        raise HTTPException(status_code=404, detail='Members not found!')
    
    return db_chat_members


@router.get('/{chat_member_id}', response_model=ChatMemberRead)
async def read_chat_member_by_id(
    db: SessionDep,
    chat_member_id: Annotated[int, Path(..., title='The chat id is required!')],
) -> Any:
    db_chat_member = await get_chat_member_by_id(db, chat_member_id)
    if not db_chat_member:
        raise HTTPException(status_code=404, detail='Chat member not found!')
    
    return db_chat_member


@router.post('/create', response_model=Message)
async def add_member(db: SessionDep, chat_member_create: ChatMemberCreate) -> Any:
    new_chat_member = await create_chat_member(db, chat_member_create)
    if not new_chat_member:
        raise HTTPException(status_code=400, detail='Something went wrong')
    
    return Message(data='User addded to the chat!')


@router.post('/create/{chat_id}', response_model=Message)
async def add_member_my(
    db: SessionDep,
    chat_id: Annotated[int, Path(..., title="The chat id is required!")],
    current_user: CurrentUser
) -> Any:
    print("ERROR HERE")
    new_chat_member = await create_chat_member_my(db, chat_id, user_id=current_user.id)
    if not new_chat_member:
        raise HTTPException(status_code=400, detail='Something went wrong')
    
    return Message(data='User addded to the chat!')


@router.delete('/remove/{chat_member_id}', response_model=Message)
async def remove_member(
    db: SessionDep,
    chat_member_id: Annotated[int, Path(..., title='The chat id is required!')],
) -> Any:
    deleted_user = await delete_chat_member(db, chat_member_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail='Member not found!')
    return Message(data='Member deleted successfully!')


@router.delete('/remove-me/{chat_id}', response_model=Message)
async def remove_member_me(
    db: SessionDep,
    current_user: CurrentUser,
    chat_id: int
) -> Any:
    deleted_user = await delete_chat_member_me(db, current_user.id, chat_id)
    print(deleted_user.id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail='Member not found!')
    return Message(data='Member deleted successfully!')