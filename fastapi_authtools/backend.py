from starlette import authentication
from starlette.requests import HTTPConnection
from pydantic import typing, BaseModel
from typing import Type

from .exceptions import Responses
from .token import decode_jwt_token


class AuthenticationBackend(authentication.AuthenticationBackend):
    def __init__(
            self,
            jwt_config: Type[BaseModel],
            excluded_urls: list | None,
            use_cookies: bool,
            user_model: Type[BaseModel],

    ):
        self.jwt_config = jwt_config
        self.use_cookies = use_cookies
        self.user_model = user_model
        self.excluded_urls = [] if excluded_urls is None else excluded_urls

    def verify_token(self, token: str):
        scopes = []
        if token is None:
            return scopes, None

        token = token.split()[-1]
        user_data = decode_jwt_token(
            token=token,
            secret_key=self.jwt_config.secret_key,
            algorithm=self.jwt_config.algorithm
        )
        if user_data is None:
            return scopes, None
        try:
            user = self.user_model(**user_data)
        except:
            raise authentication.AuthenticationError(Responses.invalid_credentials)
        else:
            return scopes, user

    def get_token(self, conn: HTTPConnection) -> str:
        if self.use_cookies:
            token = conn.cookies.get("access-token")
            return token
        else:
            token = conn.headers.get("authorization") or conn.headers.get("Authorization")
            return token

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple[authentication.AuthCredentials, authentication.BaseUser | None]]:
        if conn.url.path in self.excluded_urls:
            return authentication.AuthCredentials([]), None

        token = self.get_token(conn)
        response = self.verify_token(token)
        if isinstance(response, typing.Awaitable):
            response = await response

        scopes, user = response

        return authentication.AuthCredentials(scopes=scopes), user
