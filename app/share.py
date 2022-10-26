from os.path import join
from json import loads
from json import dumps
from secrets import token_hex
from typing import NamedTuple
from datetime import datetime
from datetime import timedelta

from flask import current_app as app

from app.utils import safe_remove

share_ttl = timedelta(hours=1)


class ShareStatus(NamedTuple):
    token: str
    created_at: int
    stopped_at: int


def get_path(filename: str) -> str:
    return join(app.drop_dir, filename + ".share")


def get_status(filename: str) -> ShareStatus or None:
    try:
        with open(get_path(filename), mode="r") as reader:
            status = ShareStatus(**loads(reader.read()))

            now = datetime.now().timestamp()

            if now >= status.stopped_at:
                remove_token(filename)
                return None

            return status
    except FileNotFoundError:
        return None


def create_token(filename: str) -> None:
    now = datetime.now()

    item = ShareStatus(
        token=token_hex(10),
        created_at=now.timestamp(),
        stopped_at=(now + share_ttl).timestamp()
    )._asdict()

    with open(get_path(filename), mode="w") as writer:
        writer.write(dumps(item))


def remove_token(filename: str) -> None:
    safe_remove(get_path(filename))
