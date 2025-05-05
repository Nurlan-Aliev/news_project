from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from app.news.likes.models import Reaction
from app.auth.crud import get_user


def set_like(news_id: int, user_id: int, session: Session):
    reaction = Reaction(news_id=news_id, user_id=user_id)
    session.add(reaction)
    session.commit()


def delete_like(reaction, session: Session):
    if reaction:
        session.delete(reaction)
        session.commit()


def get_like(news_id: int, user_id: int, session: Session):
    reaction = select(Reaction).where(
        Reaction.news_id == news_id,
        Reaction.user_id == user_id,
    )

    return session.scalar(reaction)


def get_likes(news_id: int, session: Session):
    reaction = select(Reaction).where(Reaction.news_id == news_id)
    return len(session.scalars(reaction).all())
