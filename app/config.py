import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    db_name: str = Field(env="DB_NAME")
    db_user: str = Field(env="DB_USER")
    db_password: str = Field(env="DB_PASSWORD")
    db_host: str = Field(env="DB_HOST")
    db_port: int = Field(env="DB_PORT")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def get_database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class BotSettings(BaseSettings):
    token_telegram_url: str = Field(env="TOKEN_TELEGRAM_URL")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

db_settings = DatabaseSettings()
bot_settings = BotSettings()
