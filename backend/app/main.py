from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import main

app = FastAPI(title='Smokenger')
app.include_router(main.api_router)

print(f"Project_name: {settings.PROJECT_NAME}")

origins = [
    "http://localhost:3000",  # React фронтенд
    "http://127.0.0.1:3000",    # Альтернативный localhost
    "http://192.168.56.1:3000"    
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Разрешённые источники
    allow_credentials=True,  # Разрешить куксы и авторизацию
    allow_methods=["*"],     # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],     # Разрешить все заголовки
)

@app.get("/")
async def main():
    return {"message": "Hello World"}