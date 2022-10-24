from os import remove
from os.path import join
from os.path import exists

from flask import Blueprint
from flask import current_app as app

from app.error import RedirectRequired
from app.utils import login_required

bp = Blueprint("delete", __name__, url_prefix="/delete")


@bp.get("/<string:filename>")
@login_required
def delete(filename: str):
    path = join(app.drop_dir, filename)

    if not exists(path):
        raise RedirectRequired(url="/admin?e=등록된 파일이 아닙니다.")

    remove(path)
    remove(path + ".metadata")

    raise RedirectRequired(url="/admin")
