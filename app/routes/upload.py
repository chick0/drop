from os import environ
from os.path import join
from os.path import exists
from logging import getLogger

from flask import Blueprint
from flask import request
from flask import current_app as app
from flask import render_template

from app.size import MB
from app.size import size_to_string
from app.database import create_database
from app.error import CustomError
from app.utils import safe_filename
from app.utils import safe_remove
from app.utils import get_size
from app.utils import get_flag
from app.utils import get_from

bp = Blueprint("upload", __name__, url_prefix="/")
logger = getLogger()


def get_max_size() -> int:
    size = int(environ['FILE_MAX_SIZE'])
    return size * MB


@bp.get("")
@get_flag
def front(flag: bool):
    if not flag:
        raise CustomError(
            title="권한 오류",
            message="파일 업로드 비활성화 상태입니다."
        )

    return render_template(
        "upload/form.jinja2",
        max_size=get_max_size(),
        MB=MB
    )


@bp.post("/upload")
@get_flag
def upload(flag: bool):
    def remove_self():
        safe_remove(save_path)
        safe_remove(part_path)

    if not flag:
        return "업로드 비활성화 상태입니다.", 403

    file = request.files['file']

    filename = safe_filename(file.filename)

    if not filename.endswith(".zip"):
        return "zip 파일만 업로드 할 수 있습니다.", 400

    save_path = join(app.drop_dir, filename)
    current_chunk = int(request.form['dzchunkindex'])

    if exists(save_path) and current_chunk == 0:
        return "이미 업로드된 파일입니다.", 400

    part_path = save_path + ".part"

    if not exists(part_path):
        fp = open(part_path, mode="wb")
        fp.close()

    stream = file.stream.read()

    if current_chunk == 0:
        head = stream[:3]
        if not head.startswith(b"PK"):
            return "해당 파일은 zip 파일이 아닙니다.", 400

        logger.info(f"{filename!r} uploading started by {get_from()!r}")

    total_file_size = int(request.form['dztotalfilesize'])

    if total_file_size > get_max_size():
        return f"{size_to_string(get_max_size())}보다 큰 파일을 업로드할 수 없습니다.", 400

    try:
        with open(save_path, "ab") as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(stream)
    except OSError:
        logger.exception("Fail to save uploaded file!!!")
        remove_self()
        return "파일 저장 과정에서 오류가 발생했습니다.", 500

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        size = get_size(filename)

        if size != total_file_size:
            remove_self()
            return "업로드한 파일의 크기가 일치하지 않아 취소되었습니다.", 400
        else:
            safe_remove(part_path)
            file_id = create_database(filename)
            logger.info(f"{filename!r}({file_id}) uploaded by {get_from()!r}")

    return "", 200
