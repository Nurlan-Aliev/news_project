from pydantic import BaseModel


class User(BaseModel):
    username: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
        from_attributes = True


class CreateUser(User):
    password: bytes


class ReadUser(User):
    id: int
    role: str
