from fastapi import FastAPI, Request
from functools import wraps

from pydantic import BaseModel
from typing_extensions import Awaitable

from .middleware import AuthenticationMiddleware
from .token import encode_jwt_token
from .exceptions import raise_credentials_error, raise_data_model_exception
from .models import UsernamePasswordToken


class AuthManager:
    def __init__(
            self,
            app: FastAPI,
            secret_key: str,
            algorithm: str,
            expire_minutes: int,
            create_token_model: BaseModel = UsernamePasswordToken,
    ):
        # data models
        self.create_token_model = create_token_model

        # configurations
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.expire_minutes = expire_minutes
        self._app = app

        self._configurate_app()

    @property
    def app(self) -> FastAPI:
        return self._app

    def _configurate_app(self):
        """Configurate application function (adds middleware.)"""
        self.app.add_middleware(
            AuthenticationMiddleware,
            secret_key=self.secret_key,
            expire_minutes=self.expire_minutes,
            algorithm=self.algorithm
        )

    def create_token(self, data: BaseModel) -> str:
        if not isinstance(data, self.create_token_model):
            raise_data_model_exception(self.create_token_model, data.__class__)
        return encode_jwt_token(
            user_data=data,
            secret_key=self.secret_key,
            expire_minutes=self.expire_minutes,
            algorithm=self.algorithm
        )


def login_required(func):
    """Decorator with makes view allowed only for authenticated users."""
    @wraps(func)
    def inner_view(request: Request, *args, **kwargs):
        if request.user is None:
            raise_credentials_error()
        response = func(request, *args, **kwargs)
        if isinstance(response, Awaitable):
            response = await response
        return response

    return inner_view

