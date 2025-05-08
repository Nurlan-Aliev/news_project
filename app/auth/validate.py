import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.params import Form
from sqlalchemy.orm import Session
from app.auth.crud import get_user
from app.auth.models import Users
from app.database import db_helper
from app.auth import schemas


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: Session = Depends(db_helper.session_depends),
) -> Users:
    return auth_user(username, password, session)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password
    )


def auth_user(username: str, password: str, session: Session) -> Users:
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if not (user := get_user(username, session)):
        raise unauthed_exp
    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exp
    return user


def crete_new_user(
    full_name: str = Form(),
    username: str = Form(),
    password: str = Form(),
    confirm_password: str = Form(),
):
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )
    password = hash_password(password)
    user = schemas.CreateUser(
        username=username,
        password=password,
        full_name=full_name,
    )
    return user
