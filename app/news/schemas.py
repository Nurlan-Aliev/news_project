from pydantic import BaseModel
from app.auth.schemas import User


class NewsSchemas(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True
        from_attributes = True


class ReadNewsSchemas(NewsSchemas):
    id: int
    user: User
    status: bool


class CreateNewsSchema(NewsSchemas):
    pass


class UpdateNewsSchemas(NewsSchemas):
    title: str | None = None
    content: str | None = None
