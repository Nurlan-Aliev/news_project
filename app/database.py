import secrets
from json import loads, dumps
from app.settings import settings


def get_database() -> list:
    with open(settings.db_path, "r") as f:
        result = f.read()
    return loads(result)


def create_data(user, base):
    db = get_database()
    user["id"] = len(db[base]) + 1
    db[base].append(user)
    data = dumps(db, indent=4)
    with open(settings.db_path, "w") as f:
        f.write(data)
    return user


def get_user_db(username, data):
    username_bytes = username.encode("utf8")
    database = get_database()
    for user in database[data]:
        correct_username_bytes = user["username"].encode("utf8")
        if secrets.compare_digest(correct_username_bytes, username_bytes):
            user["password"] = user["password"].encode()
            return user
