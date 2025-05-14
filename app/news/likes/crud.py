from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.news.likes.models import Reaction


def get_like(news_id: int, user_id: int, session: Session) -> Reaction:
    reaction = (
        select(Reaction)
        .where(
            Reaction.news_id == news_id,
        )
        .where(
            Reaction.user_id == user_id,
        )
    )

    return session.scalar(reaction)


def get_likes(news_id: int, like: bool, session: Session) -> int:
    reaction = (
        session.query(func.count(Reaction.news_id))
        .filter(Reaction.news_id == news_id, Reaction.like == like)
        .scalar()
    )
    return reaction


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
