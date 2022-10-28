from logging import getLogger
from datetime import datetime

from flask import Blueprint
from flask import redirect

from app.database import get_database
from app.database import set_database
from app.utils import login_required
from app.utils import get_from

bp = Blueprint("share", __name__, url_prefix="/share")
logger = getLogger()


@bp.get("/start/<string:file_id>")
@login_required
def start(file_id: str):
    database = get_database(file_id)
    database.share = True
    database.shared_at = datetime.now().timestamp()

    set_database(file_id, database)

    logger.info(f"Start {database.filename!r}({file_id}) share from {get_from()!r}")

    return redirect(f"/admin#{file_id}")


@bp.get("/stop/<string:file_id>")
@login_required
def stop(file_id: str):
    database = get_database(file_id)
    database.share = False

    set_database(file_id, database)
    logger.info(f"Stop {database.filename!r}({file_id}) share from {get_from()!r}")

    return redirect(f"/admin#{file_id}")
