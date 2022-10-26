from logging import getLogger

from flask import Blueprint
from flask import redirect

from app.share import create_token
from app.share import remove_token
from app.utils import login_required
from app.utils import get_from

bp = Blueprint("share", __name__, url_prefix="/share")
logger = getLogger()


@bp.get("/start/<string:filename>")
@login_required
def start(filename: str):
    logger.info(f"Start {filename!r} share from {get_from()!r}")
    create_token(filename)
    return redirect(f"/admin#{filename}")


@bp.get("/stop/<string:filename>")
@login_required
def stop(filename: str):
    logger.info(f"Stop {filename!r} share from {get_from()!r}")
    remove_token(filename)
    return redirect(f"/admin#{filename}")
