from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import DirectMessage
from app.schemas import DirectMessageCreate, DirectMessageUpdate
from typing import List

async def get_direct_message_by_id(db: AsyncSession, direct_message_id: int) -> DirectMessage:
    db_direct_message = await db.get(DirectMessage, direct_message_id)
    return db_direct_message

async def get_direct_messages(db: AsyncSession, sender_id: int, receiver_id: int, page = 1, limit = 50):
    offset = (page - 1) * limit
    query = (
        select(DirectMessage)
        .filter(
            ((DirectMessage.sender_id == sender_id) & (DirectMessage.receiver_id == receiver_id)) |
            ((DirectMessage.sender_id == receiver_id) & (DirectMessage.receiver_id == sender_id))
        )
        .order_by(DirectMessage.created_at.desc()) 
        .offset(offset)
        .limit(limit)
    )
    
    result = await db.execute(query)
    messages = result.scalars().all() 
    
    return messages

async def create_direct_message(
    db: AsyncSession,
    sender_id: int,
    receiver_id: int,
    direct_message_create: DirectMessageCreate
) -> DirectMessage:
    new_dirrect_message = DirectMessage(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=direct_message_create.content)
    db.add(new_dirrect_message)
    await db.commit()
    await db.refresh(new_dirrect_message)
    return new_dirrect_message

async def update_direct_message(
    db: AsyncSession,
    direct_message_id: int,
    direct_message_udpate: DirectMessageUpdate
) -> DirectMessage:
    db_direct_message = await get_direct_message_by_id(db, direct_message_id)
    if not db_direct_message:
        return None
    
    db_direct_message.content = direct_message_udpate.content
    await db.commit()
    await db.refresh(db_direct_message)
    return db_direct_message
    

async def delete_direct_message(
    db: AsyncSession,
    direct_message_id: int 
) -> DirectMessage:
    db_direct_message = get_direct_message_by_id(db, direct_message_id)
    if not db_direct_message:
        return None
    await db.delete(db_direct_message)
    await db.commit()
    return db_direct_message
