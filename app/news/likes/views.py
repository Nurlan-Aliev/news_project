from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.jwt_help import get_current_token_payload
from app.database import db_helper
from app.news.likes import crud


router = APIRouter(tags=["likes"])


@router.post("/{news_id}/like")
def set_like(
    news_id: int,
    user=Depends(get_current_token_payload),
    session: Session = Depends(db_helper.session_depends),
):
    reaction = crud.get_like(news_id, user["id"], session)
    if not reaction:
        crud.set_like(news_id, user["id"], True, session)
    elif not reaction.like:
        crud.update_like(reaction, True, session)
    return "like"


@router.delete("/{news_id}")
def delete_reaction(
    news_id,
    session: Session = Depends(db_helper.session_depends),
    user=Depends(get_current_token_payload),
):
    reaction = crud.get_like(news_id, user["id"], session)
    crud.delete_like(reaction, session)
    return "delete like"


@router.post("/{news_id}/dislike")
def set_dislike(
    news_id: int,
    user=Depends(get_current_token_payload),
    session: Session = Depends(db_helper.session_depends),
):
    reaction = crud.get_like(news_id, user["id"], session)
    if not reaction:
        crud.set_like(news_id, user["id"], False, session)
    elif reaction.like:
        crud.update_like(reaction, False, session)
    return "dislike"
