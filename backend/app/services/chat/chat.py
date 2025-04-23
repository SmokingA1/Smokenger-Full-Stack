from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc
from typing import List

from app.models import Chat, ChatMember
from app.schemas import ChatCreate, ChatUpdate


async def get_chat_by_id(db: AsyncSession, chat_id: int) -> Chat:
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    db_chat = result.scalars().first()
    if not db_chat:
        return None
    return db_chat

async def get_chats(
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
    search: str = None,
    sort: str = 'asc'
) -> List[Chat]:
    query = select(Chat)

    if search:
        query = query.where(Chat.name.ilike(f"%{search}%"))

    # сортировка по имени
    if sort == "asc":
        query = query.order_by(asc(Chat.name))
    elif sort == "desc":
        query = query.order_by(desc(Chat.name))

    offset = (page - 1) * limit
    query = query.offset(offset=offset).limit(limit=limit)

    db_chats = await db.execute(query)
    return db_chats.scalars().all()


# async def get_chats(db: AsyncSession, page: int = 1, limit: int = 20):
#     # Создаем запрос, который будет загружать чаты с их участниками и пользователями
#     query = select(Chat).options(
#         joinedload(Chat.chat_members).joinedload(ChatMember.user)  # Загрузка членов чатов и их пользователей
#     ).join(ChatMember)  # Соединяем таблицы чатов и членов чатов

#     # Пагинация
#     offset = (page - 1) * limit
#     query = query.offset(offset).limit(limit)
    
#     # Выполнение запроса
#     db_chats = await db.execute(query)
    
#     chats = db_chats.unique().all()  # Это возвращает список объектов Chat

#     # Преобразуем в Pydantic модели
#     return [ChatRead.from_orm(chat) for chat in chats]


async def get_chats_by_member_id(db: AsyncSession, member_id: int, page: int = 1, limit: int = 20) -> List[Chat]:
    query = select(Chat).join(ChatMember, ChatMember.chat_id == Chat.id).filter(ChatMember.user_id == member_id)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    db_chats = await db.execute(query)
    return db_chats.scalars().all()


async def create_chat(db: AsyncSession, chat_create: ChatCreate) -> Chat:
    new_chat = Chat(name=chat_create.name, is_private=chat_create.is_private)

    db.add(new_chat)
    try:
        await db.commit()
        await db.refresh(new_chat)
    except Exception as ex:
        await db.rollback()
        raise ex
    return new_chat

async def update_chat(db: AsyncSession, chat_id: int, chat_update: ChatUpdate) -> Chat:
    db_chat = await get_chat_by_id(db, chat_id)
    if not db_chat:
        return None

    for key, value in chat_update.dict(exclude_unset=True).items():
        setattr(db_chat, key, value)

    await db.commit()
    await db.refresh(db_chat)
    return db_chat

async def delete_chat(db: AsyncSession, chat_id: int) -> Chat:
    db_chat = await get_chat_by_id(db, chat_id)
    if not db_chat:
        return None
    
    await db.delete(db_chat)
    await db.commit()
    return db_chat
