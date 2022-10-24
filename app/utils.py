from os.path import join
from os.path import getsize
from functools import wraps

from flask import request
from flask import current_app as app
from flask import session
from flask import redirect
from user_agents import parse

from app.github import get_oauth_url


def get_size(filename: str) -> int:
    return getsize(join(app.drop_dir, filename))


def get_flag_dir() -> str:
    return join(app.base_dir, ".flag")


def get_flag(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        with open(get_flag_dir(), mode="r") as flag_reader:
            flag = flag_reader.read()

        kwargs['flag'] = True if flag == "true" else False

        return f(*args, **kwargs)

    return decorator


def set_flag(flag: bool):
    with open(get_flag_dir(), mode="w") as flag_writer:
        flag_writer.write({True: "true", False: "false"}.get(flag))


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if session['login']:
                return f(*args, **kwargs)
        except KeyError:
            pass

        return redirect(get_oauth_url())

    return decorator


def get_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr)


def get_device(user_agent: str = None) -> str:
    if user_agent is None:
        user_agent = request.user_agent.string

    ua = parse(user_agent)
    return f"{ua.get_device()} / {ua.get_os()}"
