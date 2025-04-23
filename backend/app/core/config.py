from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env',
        env_ignore_empty=True,
        extra='ignore'
    )
    SECRET_KEY: str

    PROJECT_NAME: str
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str


    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    @property
    def DATABASE_URL_async(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


    SMTP_TLS: bool = True
    SMTP_SSL: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: EmailStr | None = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    FRONTEND_HOST: str = "http://localhost:5173"

    
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)
    
settings = Settings()