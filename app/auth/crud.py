from fastapi import HTTPException, status
from fastapi.params import Form
from app.auth.database import create_user, get_user_db
from app.auth.validate import hash_password
from app.auth import schemas


def get_user(username):
    user = get_user_db(username)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')


def crete_new_user(
    first_name: str = Form(),
    last_name: str = Form(),
    username: str = Form(),
    password: str = Form(),
):

    password = hash_password(password)
    password = password.decode()
    user = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "status": "user",
    }
    user = create_user(user)
    return schemas.ReadUser(**user)
