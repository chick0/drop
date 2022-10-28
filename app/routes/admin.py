from os import listdir
from logging import getLogger

from flask import Blueprint
from flask import redirect
from flask import current_app as app
from flask import render_template

from app.database import get_database
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
    def get_size(ext: str):
        return len([
            x
            for x in listdir(app.drop_dir)
            if x.endswith(ext)
        ])

    return render_template(
        "admin/dashboard.jinja2",
        flag=flag,
        force_delete_required=len(listdir(app.data_dir)) != (get_size(".zip") - get_size(".part")),
        files=[
            file for file in [
                {
                    "id": file_id,
                    "database": get_database(file_id)
                }
                for file_id in listdir(app.data_dir)
            ]
            if file['database'] is not None
        ]
    )


@bp.get("/toggle")
@login_required
@get_flag
def toggle_status(flag: bool):
    set_flag(not flag)
    logger.info(f"Flag updated to {str(not flag).lower()!r} from {get_from()!r}")
    return redirect("/admin")
