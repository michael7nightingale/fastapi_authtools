from fastapi import FastAPI, Request, Response
from starlette.middleware import authentication
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import Awaitable, List, Callable, Type
from functools import wraps

from .middleware import AuthenticationMiddleware
from .token import encode_jwt_token
from .exceptions import raise_credentials_not_provided, raise_data_model_exception
from .models import UserModel


class JWTConfig(BaseModel):
    """JWT-tokens "configuration model."""
    secret_key: str
    algorithm: str
    expire_minutes: int


class AuthManager:
    """
    Main class of the authtools. Represent logic from adding app middleware
    to the token creation. Saves main configurations.
    """
    def __init__(
            self,
            app: FastAPI,
            secret_key: str,
            algorithm: str,
            expire_minutes: int,
            use_cookies: bool = False,
            user_model: Type[BaseModel] = UserModel,
            authorization_key: str = "authorization",
            auth_error_handler: Callable[[Request, authentication.AuthenticationError], JSONResponse] | None = None,
            excluded_urls: List[str] | None = None,
            user_getter: Callable | None = None,
            token_getter: Callable | None = None
    ):
        self._app = app
        self.jwt_config = JWTConfig(
            secret_key=secret_key,
            algorithm=algorithm,
            expire_minutes=expire_minutes
        )
        self.use_cookies = use_cookies
        self.user_model = user_model
        self.auth_error_handler = auth_error_handler
        self.excluded_urls = excluded_urls
        self.token_getter = token_getter
        self.user_getter = user_getter
        self.authorization_key = authorization_key
        self._configurate_app()

    @property
    def app(self) -> FastAPI:
        return self._app

    def login(self, response: Response, user: Type[BaseModel]) -> None:
        access_token = self.create_token(user)
        response.set_cookie(
            key=self.authorization_key,
            value=access_token,
            max_age=self.jwt_config.expire_minutes
        )

    def logout(self, response: Response) -> None:
        response.delete_cookie(self.authorization_key)

    def _configurate_app(self):
        """Configurate application function (adds middleware.)"""
        self.app.add_middleware(
            AuthenticationMiddleware,
            jwt_config=self.jwt_config,
            excluded_urls=self.excluded_urls,
            use_cookies=self.use_cookies,
            user_model=self.user_model,
            auth_error_handler=self.auth_error_handler,
            token_getter=self.token_getter,
            user_getter=self.user_getter,
            authorization_key=self.authorization_key,

        )

    def create_token(self, data: dict | BaseModel) -> str:
        """Create token function to user in token get endpoint."""
        return encode_jwt_token(
            user_data=data,
            secret_key=self.jwt_config.secret_key,
            expire_minutes=self.jwt_config.expire_minutes,
            algorithm=self.jwt_config.algorithm
        )


def login_required(func):
    """Decorator with makes view allowed only for authenticated users."""
    @wraps(func)
    async def inner_view(request: Request, *args, **kwargs):
        if request.user is None:
            raise_credentials_not_provided()
        response = func(request, *args, **kwargs)
        if isinstance(response, Awaitable):
            response = await response
        return response

    return inner_view
