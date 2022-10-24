from os import listdir
from logging import getLogger

from flask import Blueprint
from flask import redirect
from flask import current_app as app
from flask import render_template

from app.meta import get_metadata
from app.utils import get_size
from app.utils import login_required
from app.utils import get_flag
from app.utils import set_flag
from app.utils import get_from

bp = Blueprint("admin", __name__, url_prefix="/admin")
logger = getLogger()


@bp.get("")
@login_required
@get_flag
def dashboard(flag: bool):
    return render_template(
        "admin/dashboard.jinja2",
        flag=flag,
        files=[
            {
                "name": filename,
                "meta": get_metadata(filename),
                "size": get_size(filename)
            }
            for filename in listdir(app.drop_dir)
            if filename.endswith(".zip")
        ]
    )


@bp.get("/toggle")
@login_required
@get_flag
def toggle_status(flag: bool):
    set_flag(not flag)
    logger.info(f"Flag updated to {str(flag)!r} from {get_from()}")
    return redirect("/admin")
