from starlette import authentication
from starlette.datastructures import Headers
from starlette.requests import HTTPConnection
from pydantic import typing, BaseModel
from typing import Type

from .token import decode_jwt_token
from .exceptions import raise_credentials_error
from .user import FastAPIUser


class AuthenticationBackend(authentication.AuthenticationBackend):
    def __init__(
            self,
            jwt_config: Type[BaseModel],
            excluded_urls: list | None,
            user_model: Type[BaseModel],

    ):
        self.jwt_config = jwt_config
        self.user_model = user_model
        self.excluded_urls = [] if excluded_urls is None else excluded_urls

    def verify_token(self, headers: dict | Headers):
        token = headers.get("authorization") or headers.get("Authorization")
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
            raise_credentials_error()
        else:
            return scopes, user

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple[authentication.AuthCredentials, authentication.BaseUser | None]]:
        if conn.url.path in self.excluded_urls:
            return authentication.AuthCredentials([]), None

        response = self.verify_token(conn.headers)
        if isinstance(response, typing.Awaitable):
            response = await response

        scopes, user = response

        return authentication.AuthCredentials(scopes=scopes), user
