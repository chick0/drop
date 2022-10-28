from os.path import join
from os.path import exists
from logging import getLogger

from flask import Blueprint
from flask import send_file
from flask import request
from flask import session
from flask import redirect
from flask import current_app as app

from app.share import get_status
from app.utils import get_from

bp = Blueprint("download", __name__, url_prefix="/dl")
logger = getLogger()


@bp.get("/<string:filename>")
def download(filename: str):
    logined = session.get("login", False)

    if not logined:
        token = request.args.get("t", "")

        if len(token) == 0:
            return redirect("/?e=해당 파일을 다운로드할 권한이 없습니다.")

        status = get_status(filename)

        if status is None:
            return redirect("/?e=공유가 종료된 파일입니다.")

        if status.token != token:
            return redirect("/?e=인증 토큰이 올바르지 않습니다.")

    path = join(app.drop_dir, filename)

    if not exists(path):
        return redirect("/admin?e=등록된 파일이 아닙니다.")

    logger.info(f"{filename!r} file downloaded from {get_from()!r}")
    return send_file(path)
