from os.path import join
from os.path import exists

from flask import Blueprint
from flask import send_file
from flask import current_app as app

from app.error import RedirectRequired
from app.utils import login_required

bp = Blueprint("download", __name__, url_prefix="/download")


@bp.get("/<string:filename>")
@login_required
def download(filename: str):
    path = join(app.drop_dir, filename)

    if not exists(path):
        raise RedirectRequired(url="/admin?e=등록된 파일이 아닙니다.")

    return send_file(path)
