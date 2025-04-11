from datetime import datetime, UTC, timedelta
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from app.settings import settings
from app.auth.schemas import CreateUser
import jwt


http_bearer = HTTPBearer(auto_error=False)


def create_jwt(user: CreateUser) -> str:
    jwt_pyload = {"id": user["id"], "username": user["username"]}
    return encode_jwt(payload=jwt_pyload)


def encode_jwt(payload: dict):
    to_encode = payload.copy()
    utcnow = datetime.now(UTC)
    expire = utcnow + timedelta(minutes=settings.access_token_expire_min)
    to_encode.update(
        exp=expire,
        iat=utcnow,
    )

    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.algorithm)
    return encoded


def decode_jwt(token: str | bytes):
    try:
        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.algorithm]
        )
        return decoded
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_current_token_payload(
    token: HTTPBearer = Depends(http_bearer),
) -> dict:
    """returns payload from jwt"""

    try:
        payload = decode_jwt(token=token.credentials)
        return payload
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error"
        )
