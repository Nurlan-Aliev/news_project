from pydantic import BaseModel


class User(BaseModel):
    username: str
    first_name: str
    last_name: str


class CreateUser(User):
    password: str


class ReadUser(User):
    id: int
    status: str
