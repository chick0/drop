from os.path import join
from os.path import exists
from logging import getLogger

from flask import Blueprint
from flask import redirect
from flask import current_app as app

from app.utils import safe_remove
from app.utils import login_required
from app.utils import get_from

bp = Blueprint("delete", __name__, url_prefix="/delete")
logger = getLogger()


@bp.get("/<string:filename>")
@login_required
def delete(filename: str):
    path = join(app.drop_dir, filename)

    if not exists(path):
        return redirect("/admin?e=등록된 파일이 아닙니다.")

    safe_remove(path)
    safe_remove(path + ".metadata")

    logger.info(f"{filename!r} file deleted from {get_from()}")
    return redirect("/admin")
