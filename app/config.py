from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./markosdev.db"
    cors_origins: str = "*"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()