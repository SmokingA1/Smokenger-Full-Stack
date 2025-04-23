from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services.chat.message import create_chat_message, get_chat_message_by_id
from app.core.database import SessionDep
from app.schemas import ChatMessageCreate, ChatMessagePublic
from app.api.deps import CurrentUser
from typing import Dict, List
from app.services.web_socket import get_current_user_ws
import json

router = APIRouter(prefix='/ws', tags=['WebSocket'])




active_connections: Dict[str, List[WebSocket]] = {}


@router.websocket("/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, db: SessionDep, token: str = Query()):
    await websocket.accept()
    if not token:
        await websocket.close(code=1008)
        return
    current_user = await get_current_user_ws(token, db)

    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data = data.strip('"')
            chat_message_create  = ChatMessageCreate(
                chat_id=chat_id,
                sender_id=current_user.id,
                content=data
            )
            new_message = await create_chat_message(db, chat_message_create)
            print('HEREEEEEEEEEEEEE 6')

            if new_message:
                result = await get_chat_message_by_id(db, new_message.id)
                print("HERE 777777777777777777777777777777777")

                result_public = ChatMessagePublic.from_orm(result)
                print(result_public.sender.id)
                # Сериализуем Pydantic модель в JSON
                result_json = result_public.json()

                for connection in active_connections[chat_id]:
                    # if connection != websocket:
                    await connection.send_text(result_json)
                print("HEREREEEEEEEEEEEEEEE 8")

    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)
        if not active_connections[chat_id]:
            del active_connections[chat_id]