from sqlalchemy import Enum as SQLAlchemyEnum
from datetime import datetime
from pydantic import EmailStr
from app.core.database import Base
from sqlalchemy import String, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List


# User
class UserRole(Enum):
    user = 'user'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(40), index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(13), unique=True, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), default=UserRole.user)

    # chat_member = Mapped["ChatMember"] = relationship(back_populates="user")
    chat_members: Mapped[List["ChatMember"]] = relationship("ChatMember", back_populates="user")
    chat_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="sender")

#Chat
class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    is_private: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


#ChatMember
class ChatMember(Base):
    __tablename__ = 'chatmembers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'),nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


    user: Mapped["User"] = relationship("User", back_populates="chat_members")

    
#ChatMessage
class ChatMessage(Base):
    __tablename__ = 'chatmessages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    sender: Mapped["User"] = relationship("User", back_populates="chat_messages")









#DirectMessage
class DirectMessage(Base):
    __tablename__ = 'directmessages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

