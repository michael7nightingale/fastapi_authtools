import pytest
from fastapi import FastAPI
from pydantic import BaseModel


@pytest.fixture
def app():
    return FastAPI()


@pytest.fixture
def user_1_data():
    return {
        "username": "Michael",
        "password": "Password"
    }


@pytest.fixture
def create_token_model1():
    class UserCreateModel(BaseModel):
        username: str
        height: int

    return UserCreateModel
