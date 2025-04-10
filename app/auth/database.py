import secrets
from json import loads, dumps
import os


db_path = os.path.abspath('app/auth/database.json')


def get_database() -> list:
    with open(db_path, 'r') as f:
        result = f.read()
    return loads(result)


def create_user(user):
    db = get_database()
    user['id'] = len(db)+1
    db.append(user)
    data = dumps(db, indent=4)
    with open(db_path, 'w') as f:
        f.write(data)
    return user


def get_user_db(username):
    username_bytes = username.encode("utf8")
    database = get_database()
    for user in database:
        correct_username_bytes = user['username'].encode("utf8")
        if secrets.compare_digest(correct_username_bytes, username_bytes):
            user['password'] = user['password'].encode()
            return user
