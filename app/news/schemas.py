from pydantic import BaseModel, ConfigDict
from app.auth.schemas import User


class NewsSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str


class ReadNewsSchemas(NewsSchemas):
    id: int
    user: User
    status: str


class CreateNewsSchema(NewsSchemas):
    pass


class UpdateNewsSchemas(NewsSchemas):
    title: str | None = None
    content: str | None = None
