from sqlalchemy import select
from sqlalchemy.orm import Session
from app.auth.models import Users
from app.auth import schemas


def get_user(username: str, session: Session) -> Users:
    stmt = select(Users).where(Users.username == username)
    user = session.scalar(stmt)
    return user


def create_new_user(user: schemas.CreateUser, session: Session) -> Users:
    user_dict = user.model_dump()
    new_user = Users(**user_dict)
    session.add(new_user)
    session.commit()
    return new_user
