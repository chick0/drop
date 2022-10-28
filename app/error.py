from flask import render_template


class CustomError(Exception):
    def __init__(self, title: str, message: str, code: int = 400) -> None:
        super().__init__()
        self.title = title
        self.message = message
        self.code = code


def handle_custom_error(error: CustomError):
    return render_template(
        "error.jinja2",
        title=error.title,
        message=error.message
    ), error.code
