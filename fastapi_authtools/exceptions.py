from fastapi.exceptions import HTTPException


def raise_credentials_error():
    raise HTTPException(
        status_code=401,
        detail="Auth credentials are not provided."
    )


def raise_permissions_error():
    raise HTTPException(
        status_code=403,
        detail="You don`t have permissions."
    )


def raise_data_model_exception(expected, got):
    raise HTTPException(
        status_code=400,
        detail=f"""Invalid data model got: {got}. Expected: {expected}."""
    )
