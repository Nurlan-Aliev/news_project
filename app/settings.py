from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str
    access_token_expire_min: int = 36000
    algorithm: str = "HS256"

    DATABASE_PATH: str = "my_database.db"

    DEBAG: bool

    news_status: dict = {
        "confirm": "confirm",
        "reject": "reject",
        "pending": "pending",
    }

    @property
    def db_path(self):
        return f"sqlite:///{self.DATABASE_PATH}"


settings = Settings()
