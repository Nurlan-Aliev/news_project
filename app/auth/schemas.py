from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    first_name: str
    last_name: str


class CreateUser(User):
    password: bytes


class ReadUser(User):
    id: int
    role: str
