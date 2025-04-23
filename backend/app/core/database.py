from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from app.core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.DATABASE_URL_async, echo=True)
Session = async_sessionmaker(bind=engine, autoflush=False,
                             autocommit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]