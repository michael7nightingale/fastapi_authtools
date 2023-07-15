from datetime import datetime, timedelta
from typing import Type
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError


def encode_jwt_token(
        user_data: dict | Type[BaseModel],
        secret_key: str,
        algorithm: str,
        expire_minutes: int
) -> str:
    if isinstance(user_data, BaseModel):
        user_data = user_data.dict()
    user_data.update(exp=datetime.now() + timedelta(minutes=expire_minutes))
    token = jwt.encode(
        user_data,
        key=secret_key,
        algorithm=algorithm
    )
    return token


def decode_jwt_token(
        token: str,
        algorithm: str,
        secret_key: str,
) -> dict | None:
    try:
        decoded_data = jwt.decode(
            token=token,
            key=secret_key,
            algorithms=[algorithm]
        )
        return decoded_data
    except (JWTError, ValidationError):
        return None
