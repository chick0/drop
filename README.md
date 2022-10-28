# drop

간단한 파일 드롭 서버

## 설정

1. 의존성 설치
2. 깃헙 OAuth 앱 생성하기
    1. OAuth 앱은 [다음의](https://github.com/settings/applications/new) 페이지에서 생성할 수 있습니다.
    2. 생성한 앱의 "**Authorization callback URL**"을 다음과 같이 설정합니다.
        - `{APP_HOST}`/auth/callback
3. 환경 변수 설정
    ```
    CLIENT_ID       생성한 OAuth 앱의 ID
    CLIENT_SECRET   생성한 OAuth 앱의 시크릿 키
    GITHUB_USER_ID  로그인을 허용할 사용자 ID
    FILE_MAX_SIZE   업로드 가능한 최대 파일 크기 (단위: MB)
    ```
