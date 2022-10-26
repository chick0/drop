from json import loads
from json import dumps
from secrets import token_hex
from typing import NamedTuple
from datetime import datetime
from datetime import timedelta

from app.utils import get_redis

share_ttl = timedelta(hours=1)


class ShareStatus(NamedTuple):
    token: str
    created_at: int


def get_key(filename: str) -> str:
    return f"chick0/drop:{filename}"


def get_status(filename: str) -> ShareStatus or None:
    redis = get_redis()

    item = redis.get(get_key(filename))

    if item is None:
        return None

    return ShareStatus(**loads(item.decode("utf-8")))


def create_token(filename: str) -> None:
    now = datetime.now()
    redis = get_redis()

    item = ShareStatus(
        token=token_hex(36),
        created_at=now.timestamp()
    )._asdict()

    redis.set(
        get_key(filename),
        dumps(item),
        ex=share_ttl.seconds
    )


def remove_token(filename: str) -> None:
    redis = get_redis()
    redis.delete(get_key(filename))
