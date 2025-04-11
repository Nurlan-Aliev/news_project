import bcrypt
from fastapi import HTTPException, status
from fastapi.params import Form
from app.database import get_user_db


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    return auth_user(username, password)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def auth_user(login, password):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
    if not (user := get_user_db(login, "user")):
        raise unauthed_exp
    if not validate_password(password=password, hashed_password=user["password"]):
        raise unauthed_exp
    return user
