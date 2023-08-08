from datetime import datetime, timedelta
from typing import Type
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError


def encode_jwt_token(
        user_data: dict | BaseModel,
        secret_key: str,
        algorithm: str,
        expire_minutes: int
) -> str:
    if isinstance(user_data, BaseModel):
        user_data = user_data.model_dump()
    elif isinstance(user_data, dict):
        pass
    else:
        raise TypeError("Data to encode must be either `dict` ot `BaseModel`")
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
