from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class CreateUser(User):
    first_name: str
    last_name: str
    status: str


class ReadUser(CreateUser):
    id: int
