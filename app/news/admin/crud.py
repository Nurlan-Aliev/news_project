from typing import Sequence
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from app.news.models import News
from app.settings import settings


def get_pending_news(session: Session) -> Sequence[News]:
    stmt = (
        select(News)
        .where(News.status == settings.news_status["pending"])
        .order_by(desc(News.id))
    )
    all_news = session.scalars(stmt).all()
    return all_news


def get_news(idx: int, session: Session) -> News:
    stmt = select(News).where(News.id == idx)
    news = session.scalar(stmt)
    return news


def verify_news(id: int, status, session: Session) -> News:
    news = get_news(id, session)
    if news:
        news.status = status
        session.commit()
        return news
