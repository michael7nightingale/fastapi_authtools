from fastapi import HTTPException


def credentials_error_message() -> str:
    return "Auth credentials are not provided."


def permissions_error_message() -> str:
    return "You don`t have permissions."


def data_model_exception_message(expected, got) -> str:
    return f"""Invalid data model got: {got}. Expected: {expected}."""


def invalid_credentials_message() -> str:
    return "Invalid credentials provided."


def raise_credentials_error() -> str:
    raise HTTPException(
        status_code=401,
        detail=credentials_error_message()
    )


def raise_permissions_error() -> str:
    raise HTTPException(
        status_code=403,
        detail=permissions_error_message()
    )


def raise_data_model_exception(expected, got) -> str:
    raise HTTPException(
        status_code=400,
        detail=data_model_exception_message(expected, got)
    )


def raise_invalid_credentials() -> str:
    raise HTTPException(
        status_code=400,
        detail=invalid_credentials_message()
    )
