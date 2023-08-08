from fastapi import HTTPException
from enum import Enum


class Responses(str, Enum):
    credentials_not_provided = "Auth credentials are not provided."
    permission_required = "You don`t have permissions."
    invalid_credentials = "Invalid credentials provided."


def data_model_exception_message(expected, got) -> str:
    return f"""Invalid data model got: {got}. Expected: {expected}."""


def raise_credentials_not_provided() -> str:
    raise HTTPException(
        status_code=401,
        detail=Responses.credentials_not_provided
    )


def raise_permissions_error() -> str:
    raise HTTPException(
        status_code=403,
        detail=Responses.permission_required
    )


def raise_data_model_exception(expected, got) -> str:
    raise HTTPException(
        status_code=400,
        detail=data_model_exception_message(expected, got)
    )


def raise_invalid_credentials() -> str:
    raise HTTPException(
        status_code=400,
        detail=Responses.invalid_credentials
    )
