from sqlalchemy import select
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth import schemas


def get_user(username: str, session: Session) -> User:
    stmt = select(User).where(User.username == username)
    user = session.scalar(stmt)
    return user


def create_new_user(user: schemas.CreateUser, session: Session) -> User:
    user_dict = user.model_dump()
    new_user = User(**user_dict)
    session.add(new_user)
    session.commit()
    return new_user
