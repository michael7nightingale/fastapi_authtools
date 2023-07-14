from pydantic import BaseModel


class UsernamePasswordToken(BaseModel):
    """Token data model with username and password required."""
    username: str
    password: str


class UsernamePasswordEmailToken(UsernamePasswordToken):
    """Token data model with username, email and password required."""
    email: str


class EmailPasswordToken(BaseModel):
    """Token data model with email and password required."""
    email: str
    password: str


class UserModel(BaseModel):
    """Standard user request model."""
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_authenticated: bool = True
