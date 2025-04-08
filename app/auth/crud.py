from fastapi import HTTPException, status

from app.database import get_database
import secrets


def get_user(username):
    username_bytes = username.encode("utf8")
    database = get_database()
    for user in database:
        correct_username_bytes = user['username'].encode("utf8")
        if secrets.compare_digest(correct_username_bytes, username_bytes):
            user['password'] = user['password'].encode()
            return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')
