from os import mkdir
from os import environ
from os.path import join
from os.path import abspath
from os.path import dirname
from os.path import exists
from secrets import token_bytes

from flask import Flask
from flask import send_from_directory
from redis import Redis

from app.github import get_oauth_url
from app.error import RedirectRequired
from app.error import handle_redirect_required
from app.size import size_to_string


def get_key(base_dir: str) -> bytes:
    path = join(base_dir, ".SECRET_KEY")

    try:
        with open(path, mode="rb") as key_reader:
            return key_reader.read()
    except FileNotFoundError:
        new_key = token_bytes(48)
        with open(path, mode="wb") as key_writer:
            key_writer.write(new_key)

        return new_key


def create_app():
    app = Flask(__name__)
    app.base_dir = dirname(dirname(abspath(__file__)))
    app.drop_dir = join(app.base_dir, "drop")

    if not exists(app.drop_dir):
        mkdir(app.drop_dir)

    app.config['SECRET_KEY'] = get_key(app.base_dir)

    app.redis = Redis.from_url(environ['REDIS_URL'])

    from app import routes
    for route in [getattr(routes, x) for x in routes.__all__]:
        app.register_blueprint(route.bp)

    @app.get("/robots.txt")
    def robots():
        return send_from_directory(app.base_dir, "robots.txt")

    app.register_error_handler(
        code_or_exception=RedirectRequired,
        f=handle_redirect_required
    )

    def get_url(name: str) -> str:
        return {
            "oauth_login": get_oauth_url()
        }.get(name, "javascript:alert('Undefined URL name');")

    app.add_template_filter(get_url)
    app.add_template_filter(size_to_string)

    return app
