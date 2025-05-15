from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.jwt_help import get_current_token_payload
from app.database import db_helper
from app.news import schemas
from app.news import crud
from app.news.enums import Status
from app.news.read_news import read_news

router = APIRouter(tags=["News"])


@router.post("", response_model=schemas.ReadNewsSchemas)
def create_news(
    news: schemas.CreateNewsSchema,
    user=Depends(get_current_token_payload),
    session: Session = Depends(db_helper.session_depends),
):
    new_news = crud.create_news(news, user, session)
    return read_news(new_news, session)


@router.get("", response_model=list[schemas.ReadNewsSchemas])
def get_all_news(session: Session = Depends(db_helper.session_depends)):
    all_news = crud.get_all_news(session)
    return [read_news(news, session) for news in all_news]


@router.get("/{idx}", response_model=schemas.ReadNewsSchemas)
def get_news(idx: int, session: Session = Depends(db_helper.session_depends)):

    if news := crud.get_news(idx, session):
        return read_news(news, session)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{idx}", response_model=schemas.ReadNewsSchemas)
def update_news(
    idx: int,
    new_data: schemas.UpdateNewsSchemas,
    session: Session = Depends(db_helper.session_depends),
    user=Depends(get_current_token_payload),
):
    news = crud.get_news(idx, session)
    if news is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This news is not found",
        )
    if news.status == Status.confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update confirmed news",
        )
    if news.user_id != user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own news",
        )
    updated_news = crud.update_news(news, new_data, session)
    read_news(updated_news, session)
    return read_news(updated_news, session)


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
