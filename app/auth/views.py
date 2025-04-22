from app.auth import schemas
from app.auth import crud
from app.auth.jwt_help import create_jwt, get_current_token_payload
from app.auth.validate import validate_auth_user, crete_new_user
from app.database import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(tags=["Auth"])


@router.post("/sign_in")
def auth_user_issue_jwt(
    user: schemas.CreateUser = Depends(validate_auth_user),
):
    access_token = create_jwt(user)
    return access_token


@router.post("/sign_up")
def auth_user_issue_jwt(
    user: dict = Depends(crete_new_user),
    session: Session = Depends(db_helper.session_depends),
):
    new_user = crud.create_new_user(user, session)
    return schemas.ReadUser.from_orm(new_user)


@router.get("/users/me")
def read_current_user(
    credentials=Depends(get_current_token_payload),
):
    if not credentials:
        return "error"
    return {"credentials": credentials}
