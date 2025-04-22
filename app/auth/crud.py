from sqlalchemy import select
from sqlalchemy.orm import Session
from app.auth.models import User


def get_user(username: str, session: Session) -> User:
    stmt = select(User).where(User.username == username)
    user = session.scalar(stmt)
    return user


def create_new_user(user: dict, session: Session) -> User:
    new_user = User(**user)
    session.add(new_user)
    session.commit()
    return new_user
