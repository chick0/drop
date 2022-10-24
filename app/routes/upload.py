from os import remove
from os.path import join
from os.path import exists
from logging import getLogger

from flask import Blueprint
from flask import request
from flask import current_app as app
from flask import render_template
from werkzeug.utils import secure_filename

from app.utils import get_size
from app.utils import get_flag
from app.meta import create_metadata

bp = Blueprint("upload", __name__, url_prefix="/")
log = getLogger("")


@bp.get("")
def front():
    return render_template("upload/form.html")


@bp.post("/upload")
@get_flag
def upload(flag: bool):
    def remove_self():
        remove(save_path)

    if not flag:
        return "업로드 비활성화 상태입니다.", 403

    file = request.files['file']

    filename = secure_filename(file.filename)

    if "." not in filename:
        return "한글 파일명을 사용할 수 없습니다.", 400

    if not filename.endswith(".zip"):
        return "zip 파일만 업로드 할 수 있습니다.", 400

    save_path = join(app.drop_dir, filename)
    current_chunk = int(request.form['dzchunkindex'])

    if exists(save_path) and current_chunk == 0:
        return "이미 업로드된 파일입니다.", 400

    stream = file.stream.read()

    if current_chunk == 0:
        head = stream[:3]
        if not head.startswith(b"PK"):
            return "해당 파일은 zip 파일이 아닙니다.", 400

    try:
        with open(save_path, "ab") as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(stream)
    except OSError:
        log.exception("Could not write to file")
        remove_self()
        return "파일 저장 과정에서 오류가 발생했습니다.", 500

    total_chunks = int(request.form['dztotalchunkcount'])
    total_file_size = int(request.form['dztotalfilesize'])

    if current_chunk + 1 == total_chunks:
        size = get_size(filename)

        if size != total_file_size:
            log.error(f"File {filename!r} was completed, but has a size mismatch. "
                      f"Was {size} but we expected {total_file_size}.")
            remove_self()
            return "파일 크기 일치하지 않음", 500
        else:
            log.info(f"File {filename!r} has been uploaded successfully.")
            create_metadata(filename)
    else:
        log.debug(f"Chunk {current_chunk + 1} of {total_chunks} for file {filename!r} complete.")

    return "업로드 성공", 200
