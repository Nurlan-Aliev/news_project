from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.jwt_help import is_admin
from app.news.admin import crud
from app.database import db_helper
from app.news.admin import schemas
from app.news.enums import Status


router = APIRouter(tags=["Admin"], dependencies=[Depends(is_admin)])


@router.get("/pending", response_model=list[schemas.AdminNewsSchemas])
def get_pending_news(
    session: Session = Depends(db_helper.session_depends),
):

    return [
        schemas.AdminNewsSchemas.model_validate(news)
        for news in crud.get_pending_news(session)
    ]


@router.post("/{idx}/approve", response_model=schemas.AdminNewsSchemas)
def approve_news(
    idx: int, session: Session = Depends(db_helper.session_depends)
):

    news = crud.verify_news(idx, Status.confirm, session)
    if news:
        return schemas.AdminNewsSchemas.model_validate(news)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="news not found"
    )


@router.post("/{idx}/reject", response_model=schemas.AdminNewsSchemas)
def reject_news(
    idx: int, session: Session = Depends(db_helper.session_depends)
):

    news = crud.verify_news(idx, Status.reject, session)
    if news:
        return schemas.AdminNewsSchemas.model_validate(news)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="news not found"
    )
