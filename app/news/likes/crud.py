from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from app.news.likes.models import Reaction
from app.auth.crud import get_user


def get_like(news_id: int, user_id: int, session: Session) -> Reaction:
    reaction = select(Reaction).where(
        Reaction.news_id == news_id,
        Reaction.user_id == user_id,
    )
    return session.scalar(reaction)


def set_like(news_id: int, user_id: int, like: bool, session: Session) -> None:
    reaction = Reaction(news_id=news_id, user_id=user_id, like=like)
    session.add(reaction)
    session.commit()


def update_like(reaction: Reaction, like: bool, session: Session) -> None:
    reaction.like = like
    session.commit()


def delete_like(reaction, session: Session) -> None:
    if reaction:
        session.delete(reaction)
        session.commit()
