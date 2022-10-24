from os.path import join
from json import dumps
from json import loads
from typing import NamedTuple
from datetime import datetime

from flask import request
from flask import current_app as app

from app.utils import get_ip
from app.utils import get_device


class MetaData(NamedTuple):
    ip: str
    user_agent: str
    device: str
    created_at: int


def get_path(filename: str) -> str:
    return join(app.drop_dir, filename + ".metadata")


def create_metadata(filename: str) -> None:
    now = datetime.now()
    md = MetaData(
        ip=get_ip(),
        user_agent=request.user_agent.string,
        device=get_device(),
        created_at=now.timestamp()
    )

    with open(get_path(filename), mode="w") as meta_writer:
        meta_writer.write(dumps(md._asdict()))


def get_metadata(filename: str) -> MetaData:
    with open(get_path(filename), mode="r") as meta_reader:
        md = MetaData(**loads(meta_reader.read()))

    return md
