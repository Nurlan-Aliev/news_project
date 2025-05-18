from sqlalchemy.orm import Session
from app.news import schemas
from app.news.likes.crud import get_likes
from app.news.likes.schemas import LikesSchemas
from app.news.models import News


def read_news(news: News, session: Session):
    news = schemas.ReadNewsSchemas.model_validate(news)
    reaction = get_likes(news.id, session)
    reactions = LikesSchemas(
        likes=reaction["likes"],
        dislikes=reaction["dislikes"],
    )
    news.reactions_info = reactions
    return news
