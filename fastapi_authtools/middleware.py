from fastapi import FastAPI
from starlette.middleware import authentication
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import Callable, List, Type

from .backend import AuthenticationBackend


def AuthenticationMiddleware(
        app: FastAPI,
        jwt_config: Type[BaseModel],
        use_cookies: bool,
        user_model: Type[BaseModel],
        auth_error_handler: Callable[[Request, authentication.AuthenticationError], JSONResponse] | None,
        excluded_urls: List[str] | None
) -> authentication.AuthenticationMiddleware:
    """
    Fabric function that returns Auth. Middleware instance to insert
    into app middleware stack.
    """
    return authentication.AuthenticationMiddleware(
        app=app,
        backend=AuthenticationBackend(
            use_cookies=use_cookies,
            jwt_config=jwt_config,
            excluded_urls=excluded_urls,
            user_model=user_model
        ),
        on_error=auth_error_handler
    )


