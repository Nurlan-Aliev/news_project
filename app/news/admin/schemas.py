from pydantic import BaseModel, ConfigDict
from app.auth.schemas import User


class AdminNewsSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    user: User
    status: str
