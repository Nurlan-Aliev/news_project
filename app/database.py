from json import loads, dumps
import os
from app.auth.utils import next_id


db_path = os.path.abspath('app/database.json')


def get_database() -> list:
    with open(db_path, 'r') as f:
        result = f.read()
    return loads(result)


def create_user(user):
    db = get_database()
    user = user.model_dump()
    user['id'] = next_id
    user['password'] = user['password'].decode()
    db.append(user)
    data = dumps(db, indent=4)
    with open(db_path, 'w') as f:
        f.write(data)
