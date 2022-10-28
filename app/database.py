from os.path import join
from os.path import exists
from uuid import uuid4
from json import loads
from json import dumps
from datetime import datetime

from flask import current_app as app
from flask import request
from pydantic import BaseModel

from app.utils import safe_remove
from app.utils import get_size
from app.utils import get_ip
from app.utils import get_device


class Database(BaseModel):
    ip: str
    user_agent: str
    device: str
    created_at: int
    filename: str
    size: int
    share: bool
    shared_at: int


def get_path(file_id: str):
    return join(app.data_dir, file_id)


def get_new_file_id() -> str:
    while True:
        test = str(uuid4())

        if not exists(get_path(test)):
            return test


def create_database(filename: str) -> str:
    database = Database(
        ip=get_ip(),
        user_agent=request.user_agent.string,
        device=get_device(),
        created_at=datetime.now().timestamp(),
        filename=filename,
        size=get_size(filename),
        share=False,
        shared_at=0
    )

    file_id = get_new_file_id()
    path = get_path(file_id)

    with open(path, mode="w", encoding="utf-8") as db:
        db.write(dumps(database.dict()))

    return file_id


def get_database(file_id: str) -> Database or None:
    path = get_path(file_id)

    if not exists(path):
        return None

    with open(path, mode="r", encoding="utf-8") as db:
        database = Database(**loads(db.read()))

    if not exists(join(app.drop_dir, database.filename)):
        safe_remove(path)
        return None

    return database


def set_database(file_id: str, database: Database) -> bool:
    path = get_path(file_id)

    if not exists(path):
        return False

    with open(path, mode="w", encoding="utf-8") as db:
        db.write(dumps(database.dict()))

    return True
