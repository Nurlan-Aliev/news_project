from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt_help import get_current_token_payload
from app.database import db_helper
from app.news import schemas
from app.news import crud

router = APIRouter(tags=["News"])


@router.post("/", response_model=schemas.ReadNewsSchemas)
def create_new_post(
    news: schemas.CreateNewsSchema,
    user=Depends(get_current_token_payload),
    session: Session = Depends(db_helper.session_depends),
):
    new_news = crud.create_news(news, user, session)
    return schemas.ReadNewsSchemas.from_orm(new_news)


@router.get("/", response_model=list[schemas.ReadNewsSchemas])
def get_all_news(
    session: Session = Depends(db_helper.session_depends),
) -> list[schemas.ReadNewsSchemas]:
    all_news = crud.get_all_news(session)
    return [schemas.ReadNewsSchemas.from_orm(news) for news in all_news]


@router.get("/{idx}", response_model=schemas.ReadNewsSchemas)
def get_news(
    idx: int,
    session: Session = Depends(db_helper.session_depends),
):
    if news := crud.get_news(idx, session):
        return news
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{idx}", response_model=schemas.ReadNewsSchemas)
def update_news(
    idx: int,
    new_data: schemas.UpdateNewsSchemas,
    session: Session = Depends(db_helper.session_depends),
    user=Depends(get_current_token_payload),
):
    news = get_news(idx, session)
    if news is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This news is not found",
        )
    if news.status:
        raise HTTPException(
            status_code=400, detail="Cannot update confirmed news"
        )
    if news.user_id != user["id"]:
        raise HTTPException(
            status_code=403, detail="You can only edit your own news"
        )

    news = crud.update_news(news, new_data, session)
    return schemas.ReadNewsSchemas.from_orm(news)


@router.delete("/{idx}")
def delete_news(
    idx: int,
    session: Session = Depends(db_helper.session_depends),
    user=Depends(get_current_token_payload),
):
    news = get_news(idx, session)
    if news.user_id != user["id"]:
        raise HTTPException(
            status_code=403, detail="You can delete only your own news"
        )

    crud.delete_news(news, session)
    return "news was deleted"
