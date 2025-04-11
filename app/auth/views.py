from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.auth.jwt_help import create_jwt, get_current_token_payload
from app.auth.validate import validate_auth_user
from app.auth import schemas
from app.auth.crud import crete_new_user


router = APIRouter(tags=["Auth"])
http_bearer = HTTPBearer(auto_error=False)


@router.post("/sign_in")
async def auth_user_issue_jwt(
    user: schemas.CreateUser = Depends(validate_auth_user),
):
    access_token = create_jwt(user)
    return access_token


@router.post("/sign_up")
async def auth_user_issue_jwt(
    user: schemas.ReadUser = Depends(crete_new_user),
):
    return user


@router.get("/users/me")
def read_current_user(
    credentials=Depends(get_current_token_payload),
):
    if not credentials:
        return "error"
    return {"credentials": credentials}
