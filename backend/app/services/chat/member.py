from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from app.models import ChatMember
from app.schemas import ChatMemberCreate
from typing import List
from sqlalchemy.orm import selectinload


async def get_chat_members(db: AsyncSession, chat_id: int ) -> List[ChatMember]:
    db_chat_members = await db.execute(select(ChatMember).options(selectinload(ChatMember.user)).filter(ChatMember.chat_id == chat_id))
    return db_chat_members.scalars().all()



async def get_chat_member_by_id(
    db: AsyncSession,
    chat_member_id: int
) -> ChatMember:
    db_chat_member = await db.execute(select(ChatMember).options(selectinload(ChatMember.user)).where(ChatMember.id == chat_member_id))
    return db_chat_member.scalars().first()


async def get_chat_member_by_user_id(
    db: AsyncSession,
    user_id: int,
    chat_id
) -> ChatMember:
    db_chat_member = await db.execute(select(ChatMember).options(selectinload(ChatMember.user)).where((ChatMember.user_id == user_id) & (ChatMember.chat_id == chat_id)))
    return db_chat_member.scalars().first()


async def create_chat_member(db: AsyncSession, chat_member_create: ChatMemberCreate) -> ChatMember:
    new_chat_member = ChatMember(
        user_id = chat_member_create.user_id,
        chat_id = chat_member_create.chat_id
    )

    db.add(new_chat_member)
    await db.commit()
    await db.refresh(new_chat_member)
    return new_chat_member

async def create_chat_member_my(db: AsyncSession, chat_id: int, user_id: int) -> ChatMember:
    new_chat_member = ChatMember(
        user_id = user_id,
        chat_id = chat_id
    )

    db.add(new_chat_member)
    await db.commit()
    await db.refresh(new_chat_member)
    return new_chat_member


async def delete_chat_member(db: AsyncSession, chat_member_id: int) -> ChatMember:
    db_chat_member = await get_chat_member_by_id(db, chat_member_id)
    await db.delete(db_chat_member)
    await db.commit()
    return db_chat_member


async def delete_chat_member_me(db: AsyncSession, user_id: int, chat_id) -> ChatMember:

    db_member = await get_chat_member_by_user_id(db, user_id, chat_id)
    print("CHHHHHHHHHAT IDDDDDDDDDDD: ", db_member.chat_id)
    deleted_user = await delete_chat_member(db, db_member.id)
    if not deleted_user:
        return None
    return deleted_user