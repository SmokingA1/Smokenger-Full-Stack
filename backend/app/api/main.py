from fastapi import APIRouter

from app.api.routes.user import users, login, private
from app.api.routes.chat import chats, members, messages
from app.api.routes.web_socket import web_sockets
api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(private.router)
api_router.include_router(login.router)
api_router.include_router(chats.router)
api_router.include_router(messages.router)
api_router.include_router(members.router)
api_router.include_router(web_sockets.router)