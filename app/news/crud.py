from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.news import schemas
from app.auth.crud import get_user
from app.news.models import News


def create_news(data: schemas.CreateNewsSchema, user, session: Session) -> News:
    user = get_user(user["username"], session)
    new_news = News(
        title=data.title,
        content=data.content,
        user=user,
        user_id=user.id,
        status=False,
    )
    session.add(new_news)
    session.commit()
    return new_news


def get_all_news(session: Session) -> Sequence[News]:
    stmt = select(News).where(News.status)
    all_news = session.scalars(stmt).all()
    print(type(all_news))
    return all_news


def get_news(idx: int, session: Session) -> News:
    stmt = select(News).where(News.id == idx)
    news = session.scalar(stmt)
    return news
