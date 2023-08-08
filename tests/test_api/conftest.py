import pytest
from httpx import AsyncClient

from .app import app as application


@pytest.fixture
def admin() -> dict:
    return {
        "username": "admin",
        "password": "password_for_admin"
    }


@pytest.fixture
def michael7nightingale() -> dict:
    return {
        "username": "michael7nightingale",
        "password": "password"
    }


@pytest.fixture
async def app():
    yield application


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://localhost:8008") as client_:
        yield client_


@pytest.fixture
async def authorized_client(client: AsyncClient, michael7nightingale: dict):
    resp = await client.post(url_path_for("login"), json=michael7nightingale)
    access_token = resp.json()['access-token']
    client.headers['Authorization'] = f"Token {access_token}"
    yield client


url_path_for = lambda name, **kwargs: application.url_path_for(name, **kwargs)
