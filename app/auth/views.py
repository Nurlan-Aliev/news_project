from app.auth import schemas
from app.auth import crud
from app.auth.jwt_help import create_jwt, get_current_token_payload, is_admin
from app.auth.validate import validate_auth_user, crete_new_user
from app.database import db_helper
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


router = APIRouter(tags=["Auth"])


@router.post("/sign_in")
def auth_user_issue_jwt(
    user: schemas.ReadUser = Depends(validate_auth_user),
):
    access_token = create_jwt(user)
    return access_token


@router.post("/sign_up")
def auth_user_issue_jwt(
    new_user: schemas.CreateUser = Depends(crete_new_user),
    session: Session = Depends(db_helper.session_depends),
):
    user = crud.get_user(new_user.username, session)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    new_user = crud.create_new_user(new_user, session)
    return schemas.ReadUser.from_orm(new_user)
