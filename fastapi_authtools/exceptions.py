from fastapi.exceptions import HTTPException


HTTPException401 = HTTPException(status_code=401, detail="Auth credentials are not provided.")
HTTPException403 = HTTPException(status_code=403, detail="You don`t have permissions.")
