from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    DATABASE_PATH: str
    DEBAG: bool
    ORIGIN: list[str]

    news_status: dict = {
        "confirm": "confirm",
        "reject": "reject",
        "pending": "pending",
    }

    @property
    def db_path(self):
        return f"sqlite:///{self.DATABASE_PATH}"


settings = Settings()
