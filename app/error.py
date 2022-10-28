from flask import redirect
from flask import render_template


class RedirectRequired(Exception):
    def __init__(self, url: str, code: int = 302) -> None:
        super().__init__()
        self.url = url
        self.code = code


def handle_redirect_required(error: RedirectRequired):
    return redirect(error.url, error.code)


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
