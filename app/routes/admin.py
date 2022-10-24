from os import listdir

from flask import Blueprint
from flask import redirect
from flask import current_app as app
from flask import render_template

from app.utils import get_size
from app.utils import login_required
from app.utils import get_flag
from app.utils import set_flag
from app.meta import get_metadata

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("")
@login_required
@get_flag
def dashboard(flag: bool):
    return render_template(
        "admin/dashboard.html",
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
    return redirect("/admin")
