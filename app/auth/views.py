from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.jwt_help import create_jwt, decode_jwt
from app.auth.validate import validate_auth_user
from app.auth import schemas
from app.database import create_user
from app.auth.validate import hash_password


router = APIRouter(tags=['Auth'])
http_bearer = HTTPBearer()


@router.post("/sign_in")
async def auth_user_issue_jwt(
    user: schemas.CreateUser = Depends(validate_auth_user),
):
    access_token = create_jwt(user)
    return access_token


@router.post("/sign_up")
async def auth_user_issue_jwt(
    user: schemas.CreateUser,
):
    user.password = hash_password(user.password)
    create_user(user)
    return 'user was created'


@router.get("/users/me")
def read_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    if not credentials:
        return "error"
    return {"credentials": decode_jwt(credentials.credentials)}
