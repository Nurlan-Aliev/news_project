from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.jwt_help import get_current_token_payload
from app.database import db_helper
from app.news.likes import crud


router = APIRouter(tags=["likes"])


@router.post("/{news_id}")
def set_like(
    news_id: int,
    user=Depends(get_current_token_payload),
    session: Session = Depends(db_helper.session_depends),
):
    if not crud.get_like(news_id, user["id"], session):
        crud.set_like(news_id, user["id"], session)
    return "like"


@router.delete("/{news_id}")
def delete_like(
    news_id,
    session: Session = Depends(db_helper.session_depends),
    user=Depends(get_current_token_payload),
):
    reaction = crud.get_like(news_id, user["id"], session)
    crud.delete_like(reaction, session)
    return "delete like"
