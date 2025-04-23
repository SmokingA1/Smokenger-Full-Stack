from pydantic import EmailStr, BaseModel, Field
from typing import Optional, List
from datetime import datetime 

#User
class UserBase(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=40)
    email: EmailStr = Field(..., min_length=4, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=13)
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=30)


class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=30)

    class Config:
        str_min_length = 1


class UserRegisterPrivate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    email: EmailStr = Field(..., min_length=4, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=13)
    password: str = Field(..., min_length=8, max_length=30)

    
class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, max_length=255)  # type: ignore
    password: Optional[str] = Field(None, min_length=8, max_length=40)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserUpdateMe(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=40)
    email: Optional[EmailStr] = Field(None, min_length=4, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=13)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserUpdateName(BaseModel):
    new_name: str = Field(..., min_length=1, max_length=40)


class UserUpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=30)
    new_password: str = Field(..., min_length=8, max_length=30)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserPublic(UserBase):
    id: int

    class Config:
        from_attributes = True

    
#ChatMember
class ChatMemberBase(BaseModel):
    user_id: int = Field(...)
    chat_id: int = Field(...)
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMemberCreate(ChatMemberBase):
    pass


class ChatMemberRead(ChatMemberBase):
    id: int
    user: UserPublic
    class Config:
        from_attributes = True

#Chat 
class ChatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_private: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: int
    class Config:
        from_attributes = True


class ChatUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)

#ChatMessage
class ChatMessageBase(BaseModel):
    chat_id: int = Field(...)
    sender_id: int = Field(default=None,)
    content: str = Field(..., min_length=1, max_length=1500)


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageRead(ChatMessageBase):
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class ChatMessagePublic(BaseModel):
    id: int 
    sender_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    sender: UserPublic

    class Config:
        from_attributes = True


class ChatMessageUpdate(BaseModel):
    content: str = Field(None, min_length=1, max_length=1500)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

#DirectMessage
class DirectMessageBase(BaseModel):
    sender_id: int = Field(...)
    receiver_id: int = Field(...)
    content: str = Field(..., min_length=1, max_length=1500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DirectMessageCreate(DirectMessageBase):
    pass


class DirectMessageRead(DirectMessageBase):
    id: int

    class Config:
        from_attributes = True


class DirectMessageUpdate(BaseModel):
    content: str = Field(None, min_length=1, max_length=1500)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DirectMessagePublic(BaseModel):
    sender_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

#Different
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    sub: str | None = None 
    exp: float


class Message(BaseModel):
    data: str