from os import environ
from typing import NamedTuple

from dotenv import load_dotenv
from requests import get
from requests import post

from app.error import RedirectRequired

if "CLIENT_ID" not in environ:
    load_dotenv()

CLIENT_ID = environ['CLIENT_ID']
CLIENT_SECRET = environ['CLIENT_SECRET']
GITHUB_USER_ID = int(environ['GITHUB_USER_ID'])


class GithubUser(NamedTuple):
    login: str
    id: int


def get_oauth_url() -> str:
    return "https://github.com/login/oauth/authorize?" + \
        "client_id=" + CLIENT_ID


def get_access_token(code: str) -> str:
    response = post(
        url="https://github.com/login/oauth/access_token",
        headers={
            "Accept": "application/json",
            "User-Agent": "DropAPP Github OAuth"
        },
        json={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        }
    )

    json = response.json()

    try:
        return json['access_token']
    except KeyError:
        raise RedirectRequired(url=get_oauth_url())


def get_user(token: str) -> GithubUser:
    response = get(
        url="https://api.github.com/user",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}"
        }
    )

    if response.ok:
        json = response.json()

        return GithubUser(
            login=json['login'],
            id=json['id']
        )
    else:
        raise RedirectRequired(url=get_oauth_url())
