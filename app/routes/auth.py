from logging import getLogger

from flask import Blueprint
from flask import request
from flask import session
from flask import redirect

from app.github import GITHUB_USER_ID
from app.github import get_access_token
from app.github import get_user
from app.utils import get_from

bp = Blueprint("auth", __name__, url_prefix="/auth")
logger = getLogger()


@bp.get("/callback")
def callback():
    code = request.args.get("code", "")

    if len(code) == 0:
        return redirect("/?e=코드가 올바르지 않습니다.")

    token = get_access_token(code)
    user = get_user(token)

    if user.id == GITHUB_USER_ID:
        session['login'] = True
        logger.info(f"{user.login!r} login in from {get_from()!r}")
        return redirect("/admin")
    else:
        logger.info(f"{user.login!r} try to login in from {get_from()!r}")
        return redirect("/?e=해당 계정은 관리자가 아닙니다.")
