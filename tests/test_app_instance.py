import pytest

from fastapi_authtools import AuthManager


def test_adding_middleware(app):
    len_user_middleware_before = len(app.user_middleware) if app.user_middleware is not None else 0
    AuthManager(
        app=app,
        algorithm="HS256",
        secret_key="Asd-adsa",
        expire_minutes=120
    )
    assert len(app.user_middleware) - len_user_middleware_before == 1
