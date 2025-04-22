import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.params import Form
from sqlalchemy.orm import Session
from app.auth.crud import get_user
from app.auth.models import User
from app.database import db_helper


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: Session = Depends(db_helper.session_depends),
) -> User:
    return auth_user(username, password, session)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def auth_user(username: str, password: str, session: Session) -> User:
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
    if not (user := get_user(username, session)):
        raise unauthed_exp
    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exp
    return user


def crete_new_user(
    first_name: str = Form(),
    last_name: str = Form(),
    username: str = Form(),
    password: str = Form(),
):

    password = hash_password(password)
    user = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "status": "user",
    }
    return user
