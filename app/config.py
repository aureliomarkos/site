from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./markosdev.db"
    cors_origins: str = "*"
    admin_password: str = "admin123"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()