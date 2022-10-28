from os.path import join
from logging import getLogger

from flask import Blueprint
from flask import session
from flask import send_file
from flask import current_app as app

from app.database import get_database
from app.utils import get_from

bp = Blueprint("download", __name__, url_prefix="/dl")
logger = getLogger()


@bp.get("/<string:file_id>")
def download(file_id: str):
    admin: bool = session.get("login", False)
    database = get_database(file_id)

    if database is None:
        return "등록된 파일이 아닙니다."

    if not admin:
        if not database.share:
            return "해당 파일은 공유가 비활성화된 상태입니다."

    logger.info(f"{database.filename!r}({file_id}) downloaded from {get_from()!r}")
    return send_file(join(app.drop_dir, database.filename))
