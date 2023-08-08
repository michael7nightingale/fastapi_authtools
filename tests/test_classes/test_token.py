import pytest
from pydantic import BaseModel


class UserData(BaseModel):
    x: int
    y: int


class TestCreateToken:

    async def test_create_token_success_dict(self, auth_manager):
        user_data = {
            "username": "asdas",
            "email": 'dsasfa@mail.ru'
        }
        token = auth_manager.create_token(user_data)
        assert isinstance(token, str)

    async def test_create_token_success_pydantic_model(self, auth_manager):
        user_data = UserData(x=12, y=123)
        token = auth_manager.create_token(user_data)
        assert isinstance(token, str)

    async def test_create_token_success_fail_type_int(self, auth_manager):
        user_data = 1203918209471209481
        with pytest.raises(TypeError):
            token = auth_manager.create_token(user_data)

    async def test_create_token_success_fail_type_str(self, auth_manager):
        user_data = "1203918209471209481"
        with pytest.raises(TypeError):
            token = auth_manager.create_token(user_data)
