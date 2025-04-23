from fastapi import Depends, HTTPException, APIRouter, Path, Query
from app.schemas import ChatMessageCreate, ChatMessagePublic, ChatMessageUpdate, ChatMessageRead, Message
from app.services.chat.chat import get_chat_by_id
from app.services.chat.message import (
    get_chat_message_by_id,
    get_chat_messages_with_sender,
    create_chat_message,
    update_chat_message,
    delete_chat_message
)
from app.core.database import SessionDep
from typing import Any, List, Annotated
from app.api.deps import CurrentUser
router = APIRouter(prefix='/chat-messages', tags=['ChatMessage'])

@router.get('/{chat_id}', response_model=List[ChatMessagePublic])
async def read_messages_with_sender(
    db: SessionDep, chat_id: Annotated[int, Path(..., title='The chat id is required!')],
    offset: int = Query(0, title="Page number is required")) -> Any:
    db_chat = await get_chat_by_id(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail='Chat not found!')
    db_chat_messages = await get_chat_messages_with_sender(db, chat_id, offset=offset)
    if not db_chat_messages:
        raise HTTPException(status_code=404, detail='There are not messages yet!')
    return db_chat_messages


@router.get('/one/{chat_message_id}/', response_model=ChatMessagePublic)
async def read_chat_message_by_id(
    db: SessionDep,
    chat_message_id: Annotated[int, Path(..., title='The chat message id is required!')]
) -> Any:
    db_chat_message = await get_chat_message_by_id(db, chat_message_id)
    if not db_chat_message:
        raise HTTPException(status_code=404, detail='Message not found!')
    return db_chat_message


@router.post('/create', response_model=ChatMessagePublic)
async def create_message(db: SessionDep, chat_message_create: ChatMessageCreate, current_user: CurrentUser) -> Any:
    chat_message_create.sender_id = current_user.id 
    print("HEREEEEEEEEEEEEEEEE 3")

    new_chat_message = await create_chat_message(db, chat_message_create, )
    if not new_chat_message:
        raise HTTPException(status_code=400, detail='Something went wrong')
    
    new_chat_message_with_sender = await get_chat_message_by_id(db, new_chat_message.id)
    
    # Отправляем ответ с новым сообщением
    return new_chat_message_with_sender


@router.put('/update/{chat_message_id}', response_model=Message)
async def update_existing_message(
    db: SessionDep,
    chat_message_id: Annotated[int, Path(..., title='The chat message id is required!')],
    chat_message_update: ChatMessageUpdate
) -> Any:
    db_chat_message = await get_chat_message_by_id(db, chat_message_id)
    if not db_chat_message:
        raise HTTPException(status_code=404, detail='Message not found!')
    updated_chat_message = await update_chat_message(db, chat_message_id, chat_message_update)
    if not updated_chat_message:
        raise HTTPException(status_code=404, detail='Somthing went wrong!')
    return Message(data='Message updated successfully!')


@router.delete('/delete/{chat_message_id}', response_model=Message)
async def delete_existing_message(
    db: SessionDep,
    chat_message_id: Annotated[int, Path(..., title='The chat message id is required!')]
) -> Any:
    db_chat_message = await get_chat_message_by_id(db, chat_message_id)
    if not db_chat_message:
        raise HTTPException(status_code=404, detail='Message not found!')
    deleted_chat_message = await delete_chat_message(db, chat_message_id)
    if not deleted_chat_message:
        raise HTTPException(status_code=400, detail='Something went wrong!')
    return Message(data='Message deleted successfully!')
