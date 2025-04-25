from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.jwt_help import is_admin
from app.news.admin import crud
from app.database import db_helper
from app.news import schemas
from app.settings import settings


router = APIRouter(tags=["Admin"], dependencies=[Depends(is_admin)])


@router.get("/pending", response_model=list[schemas.ReadNewsSchemas])
def get_pending_news(
    session: Session = Depends(db_helper.session_depends),
):

    return [
        schemas.ReadNewsSchemas.from_orm(news)
        for news in crud.get_pending_news(session)
    ]


@router.post("/{idx}/approve", response_model=schemas.ReadNewsSchemas)
def approve_news(
    idx: int, session: Session = Depends(db_helper.session_depends)
):

    news = crud.verify_news(idx, settings.news_status["confirm"], session)
    if news:
        return schemas.ReadNewsSchemas.from_orm(news)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="news not found"
    )


@router.post("/{idx}/reject", response_model=schemas.ReadNewsSchemas)
def reject_news(
    idx: int, session: Session = Depends(db_helper.session_depends)
):

    news = crud.verify_news(idx, settings.news_status["reject"], session)
    if news:
        return schemas.ReadNewsSchemas.from_orm(news)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="news not found"
    )
