from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models import ChatMessage
from app.schemas import ChatMessageCreate, ChatMessageUpdate
from typing import List


# async def get_chat_messages(db: AsyncSession, chat_id: int, page: int = 1, limit: int = 50) -> List[ChatMessage]:
#     offset = (page - 1) * limit
#     query = (
#         select(ChatMessage)
#         .filter(ChatMessage.chat_id == chat_id)
#         .order_by(ChatMessage.created_at.desc())
#         .offset(offset=offset)
#         .limit(limit=limit)
#     )
#     db_messages = await db.execute(query)
#     return db_messages.scalars().all()



# async def get_chat_messages_with_sender(db: AsyncSession, chat_id: int, page: int = 1, limit: int = 20) -> List[ChatMessage]:
#     offset = (page - 1) * limit
#     print(page)
#     print(offset)
#     print(limit)
#     query = (
#         select(ChatMessage)
#         .options(joinedload(ChatMessage.sender))
#         .filter(ChatMessage.chat_id == chat_id)
#         .order_by(ChatMessage.created_at.desc())
#         .offset(offset=offset)
#         .limit(limit=limit)
#     )
#     db_messages = await db.execute(query)
#     return db_messages.scalars().all()



async def get_chat_messages_with_sender(db: AsyncSession, chat_id: int, offset: int, limit: int = 20)-> List[ChatMessage]:
    # total_count = await db.execute

    query = (
        select(ChatMessage)
        .options(joinedload(ChatMessage.sender))
        .filter(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    db_messages = await db.execute(query)
    return db_messages.scalars().all()



async def get_chat_message_by_id(db: AsyncSession, chat_message_id: int) -> ChatMessage:
    query = select(ChatMessage).options(joinedload(ChatMessage.sender)).where(ChatMessage.id == chat_message_id)

    # Выполняем запрос
    result = await db.execute(query)

    db_chat_message = result.scalars().first()

    return db_chat_message


async def create_chat_message(db: AsyncSession, chat_message_create: ChatMessageCreate) -> ChatMessage:
    print("HEREEEEEEEEEEEEEEEE 1")
    new_chat_message = ChatMessage(
        chat_id=chat_message_create.chat_id,
        sender_id=chat_message_create.sender_id,
        content=chat_message_create.content
    )

    # new_chat_message = ChatMessage(**chat_message_create.dict())
    print(new_chat_message.chat_id)
    print("HEREEEEEEEEEEEEEEEE 2")

    db.add(new_chat_message)
    print("HEREEEEEEEEEEEEEEEEE 3")
    await db.commit()
    print("HEREEEEEEEEEEEEEEEEE 4")

    await db.refresh(new_chat_message)
    print("HEREEEEEEEEEEEEEEEEE 5")

    return new_chat_message
    


async def update_chat_message(
    db: AsyncSession,
    chat_message_id: int,
    chat_message_update: ChatMessageUpdate
) -> ChatMessage:
    chat_message = await get_chat_message_by_id(db, chat_message_id)
    if not chat_message:
        return None
    
    if chat_message_update.content:
        chat_message.content = chat_message_update.content

    db.commit()
    db.refresh(chat_message)
    return chat_message

async def delete_chat_message(db: AsyncSession, chat_message_id: int) -> ChatMessage:
    chat_message = await get_chat_message_by_id(db, chat_message_id)
    if not chat_message:
        return None
    
    await db.delete(chat_message)
    await db.commit()
    return chat_message