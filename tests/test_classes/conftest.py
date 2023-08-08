import pytest
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_authtools import AuthManager


@pytest.fixture
def app() -> FastAPI:
    return FastAPI()


@pytest.fixture
def auth_manager(app) -> AuthManager:
    return AuthManager(
        app=app,
        algorithm="HS256",
        secret_key="Asd-adsa",
        expire_minutes=120
    )


@pytest.fixture
def user_1_data() -> dict:
    return {
        "username": "Michael",
        "password": "Password"
    }
