from sqlalchemy.orm import Session
from app.news import schemas
from app.news.likes.crud import get_likes, get_like
from app.news.likes.schemas import LikesSchemas
from app.news.models import News


def read_news(news: News, user, session: Session):

    if user:
        user = get_like(news_id=news.id, user_id=user["id"], session=session)
        user = user.like

    news = schemas.ReadNewsSchemas.model_validate(news)

    reaction = get_likes(news.id, session)

    reactions = LikesSchemas(
        likes=reaction["likes"],
        dislikes=reaction["dislikes"],
        user_reaction=user,
    )

    news.reactions_info = reactions
    return news
