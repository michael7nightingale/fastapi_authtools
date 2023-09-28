from starlette import authentication
from starlette.requests import HTTPConnection
from pydantic import typing, BaseModel
from typing import Type, Callable, Awaitable

from .exceptions import Responses
from .token import decode_jwt_token


class AuthenticationBackend(authentication.AuthenticationBackend):
    def __init__(
            self,
            jwt_config: Type[BaseModel],
            excluded_urls: list | None,
            use_cookies: bool,
            user_model: Type[BaseModel],
            authorization_key: str = "authorization",
            user_getter: Callable | None = None,
            token_getter: Callable | None = None
    ):
        self.jwt_config = jwt_config
        self.use_cookies = use_cookies
        self.user_model = user_model
        self.token_getter = token_getter
        self.user_getter = user_getter
        self.authorization_key = authorization_key
        self.excluded_urls = [] if excluded_urls is None else excluded_urls

    async def verify_token(self, token: str):
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
            if self.user_getter is not None:
                user = self.user_getter(**user.model_dump())
                if isinstance(user, Awaitable):
                    user = await user
            return scopes, user

    def get_token(self, conn: HTTPConnection) -> str:
        if self.use_cookies:
            token = conn.cookies.get(self.authorization_key)
            return token
        else:
            token = conn.headers.get(self.authorization_key)
            return token

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple[authentication.AuthCredentials, authentication.BaseUser | None]]:
        if conn.url.path in self.excluded_urls:
            return authentication.AuthCredentials([]), None
        if self.token_getter is None:
            token = self.get_token(conn)
        else:
            token = self.token_getter(conn)
            if isinstance(token, Awaitable):
                token = await token
        response = await self.verify_token(token)
        if isinstance(response, typing.Awaitable):
            response = await response

        scopes, user = response

        return authentication.AuthCredentials(scopes=scopes), user
