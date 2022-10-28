from os.path import join
from os.path import exists
from logging import getLogger

from flask import Blueprint
from flask import redirect
from flask import current_app as app

from app.database import get_database
from app.utils import safe_remove
from app.utils import login_required
from app.utils import get_from

bp = Blueprint("delete", __name__, url_prefix="/delete")
logger = getLogger()


@bp.get("/<string:file_id>")
@login_required
def delete(file_id: str):
    path = join(app.data_dir, file_id)

    if not exists(path):
        return redirect("/admin?e=등록된 파일이 아닙니다.")

    database = get_database(file_id)

    safe_remove(path)
    safe_remove(join(app.drop_dir, database.filename))

    logger.info(f"{database.filename!r}({file_id}) file deleted from {get_from()!r}")
    return redirect("/admin")
