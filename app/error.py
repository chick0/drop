from flask import redirect


class RedirectRequired(Exception):
    def __init__(self, url: str, code: int = 302) -> None:
        super().__init__()
        self.url = url
        self.code = code


def handle_redirect_required(error: RedirectRequired):
    return redirect(error.url, error.code)
