from datetime import datetime, UTC, timedelta
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from app.settings import settings
from app.auth.schemas import ReadUser
import jwt


http_bearer = HTTPBearer(auto_error=False)


def create_jwt(user: ReadUser) -> str:
    jwt_pyload = {
        "id": user.id,
        "username": user.username,
        "fullname": user.full_name,
        "role": user.role,
    }
    return encode_jwt(payload=jwt_pyload)


def encode_jwt(payload: dict):
    to_encode = payload.copy()
    utcnow = datetime.now(UTC)
    expire = utcnow + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        exp=expire,
        iat=utcnow,
    )

    encoded = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded


def decode_jwt(token: str | bytes):
    try:
        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error",
        )


def get_current_token_payload(
    token: HTTPBearer = Depends(http_bearer),
) -> dict:
    try:
        payload = decode_jwt(token=token.credentials)
        return payload
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="need to log in "
        )


def is_admin(token: HTTPBearer = Depends(http_bearer)):
    try:
        payload = decode_jwt(token=token.credentials)
        if payload.get("role") == "admin":
            return payload
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have permissions",
        )
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="need to log in "
        )
