from os import environ
from typing import NamedTuple

from dotenv import load_dotenv
from requests import get
from requests import post

from app.error import CustomError

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
        raise CustomError(
            title="인증 오류",
            message="인증 토큰을 불러올 수 없습니다.",
            code=403
        )


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
        raise CustomError(
            title="인증 오류",
            message="OAuth 서버에서 사용자 정보를 불러오지 못했습니다.",
            code=403
        )
