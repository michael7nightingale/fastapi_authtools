from fastapi import FastAPI, Request
from starlette.middleware import authentication
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import Awaitable, List, Callable
from functools import wraps

from .middleware import AuthenticationMiddleware
from .token import encode_jwt_token
from .exceptions import raise_credentials_error, raise_data_model_exception
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
            user_model: BaseModel = UserModel,
            auth_error_handler: Callable[[Request, authentication.AuthenticationError], JSONResponse] | None = None,
            excluded_urls: List[str] | None = None
    ):
        self._app = app
        self.jwt_config = JWTConfig(
            secret_key=secret_key,
            algorithm=algorithm,
            expire_minutes=expire_minutes
        )
        self.user_model = user_model
        self.auth_error_handler = auth_error_handler
        self.excluded_urls = excluded_urls

        self._configurate_app()

    @property
    def app(self) -> FastAPI:
        return self._app

    def _configurate_app(self):
        """Configurate application function (adds middleware.)"""
        self.app.add_middleware(
            AuthenticationMiddleware,
            jwt_config=self.jwt_config,
            excluded_urls=self.excluded_urls,
            user_model=self.user_model,
            auth_error_handler=self.auth_error_handler
        )

    def create_token(self, data: BaseModel) -> str:
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
            raise_credentials_error()
        response = func(request, *args, **kwargs)
        if isinstance(response, Awaitable):
            response = await response
        return response

    return inner_view
