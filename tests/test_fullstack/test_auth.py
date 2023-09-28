import pytest
from fastapi import status
from httpx import AsyncClient

from .conftest import url_path_for


class TestLogin:

    async def test_login_success(self, client: AsyncClient, michael7nightingale: dict):
        resp = await client.post(url_path_for("login_post"), data=michael7nightingale)
        assert resp.status_code == status.HTTP_303_SEE_OTHER
        assert "authorization" in resp.cookies

    async def test_login_fail(self, client: AsyncClient):
        user_data = {
            "username": "string",
            "password": "string_password"
        }
        resp = await client.post(url_path_for("login_post"), data=user_data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "access-token" not in resp.json()
        assert resp.json() == {"detail": "Cannot find user with this credentials."}

    async def test_login_fail_password_invalid(self, client: AsyncClient, admin):
        user_data = {
            "username": admin['username'],
            "password": "string_password_+asdas"
        }
        resp = await client.post(url_path_for("login_post"), data=user_data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "access-token" not in resp.json()
        assert resp.json() == {"detail": "Password is invalid."}


class TestMeLoginRequired:

    async def test_me_success(self, authorized_client: AsyncClient):
        resp = await authorized_client.get(url_path_for("me"))
        assert resp.status_code == status.HTTP_200_OK

    async def test_me_fail_tokenless(self, client: AsyncClient):
        resp = await client.get(url_path_for("me"))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert resp.json() == {"detail": 'Auth credentials are not provided.'}

    async def test_me_fail_token_invalid(self, client: AsyncClient):
        client.headers['Authorization'] = "Token 124-i0lfkajnlfksajkfs;ai 0f-aojnf"
        resp = await client.get(url_path_for("me"))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert resp.json() == {"detail": 'Auth credentials are not provided.'}
