from fastapi import HTTPException, APIRouter, Query, Path

from app.core.database import SessionDep
from app.schemas import ChatCreate, ChatRead, ChatUpdate, Message
from app.services.chat.chat import (
    get_chat_by_id,
    get_chats,
    create_chat,
    update_chat,
    delete_chat,
    get_chats_by_member_id
)
from app.services.chat.member import create_chat_member_my

from app.api.deps import CurrentUser
from typing import List, Any, Annotated

import asyncio

router = APIRouter(prefix='/chats', tags=['Chat'])

@router.get('/', response_model=List[ChatRead])
async def read_chats(
    db: SessionDep,
    page: int = Query(1, title='The number of page is required'),
    limit: int = Query(20, title='The quantity of chats is required!'),
    search: str = Query(None, title="The chat only chat name is required!"),
    sort: str = Query('asc', title="Type sort is required - asc or desc")
) -> Any:
    db_chats = await get_chats(db, page, limit, search=search, sort=sort)
    if not db_chats:
        raise HTTPException(status_code=404, detail='Chats not found!')
    return db_chats

@router.get("/my/", response_model=List[ChatRead])
async def read_chats_by_member_id(
    db: SessionDep,
    current_user: CurrentUser,
    page: int = Query(1, title='The number of page is required'),
    limit: int = Query(20, title='The quantity of chats is required!')
) -> Any:
    db_chats = await get_chats_by_member_id(db, member_id=current_user.id, page=page, limit=limit)
    if not db_chats:
        raise HTTPException(status_code=404, detail='Chats not found!')
    return db_chats


@router.get('/{chat_id}', response_model=ChatRead)
async def read_chat_by_id(
    db: SessionDep,
    chat_id: Annotated[int, Path(..., title='The chat id is required!')]
) -> Any:
    db_chat = await get_chat_by_id(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail='Chat not found!')
    #next row is under question
    return ChatRead.model_validate(db_chat)

@router.post('/create', response_model=ChatRead)
async def add_chat(db: SessionDep, chat_create: ChatCreate) -> Any:
    """
    Add new chat
    """
    new_chat = await create_chat(db, chat_create)

    if not new_chat:
        raise HTTPException(status_code=400, detail='Something went wrong!')
    
    return new_chat




@router.put('/update/{chat_id}', response_model=Message)
async def update_existing_chat(
    db: SessionDep,
    chat_id: Annotated[int, Path(..., title='The chat id is required!')],
    chat_update: ChatUpdate
) -> Any:
    db_chat = await get_chat_by_id(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail='Chat not found!')
    updated_chat = await update_chat(db, chat_id, chat_update)
    if not updated_chat:
        raise HTTPException(status_code=422, detail='Error input data!')
    return Message(data='Chat updated successfully!')

@router.delete('/delete/{chat_id}', response_model=Message)
async def delete_existing_chat(db: SessionDep, chat_id: Annotated[int, Path(..., title='The chat id is required!')]) -> Any:
    db_chat = await get_chat_by_id(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail='Chat not found!')
    
    deleted_chat = await delete_chat(db, chat_id)
    if not deleted_chat:
        raise HTTPException(status_code=400, detail='Somthing went wrong!')
    return Message(data='Chat deleted successfully!')
