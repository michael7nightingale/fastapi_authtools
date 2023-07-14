# FastAPI auth library.

It`s simple to connect to your project. Just make user_data verification, and library will manage JWT-tokens.

## Installation
Install package with pip:
```commandline
pip install fastapi-authtools
```

...or with poetry:
```commandline
poetry add fastapi-authtools
```

## Usage
```python
from fastapi import FastAPI, Request, Body
from fastapi import FastAPI, Request, Body

from fastapi_authtools import AuthManager, login_required
from fastapi_authtools.models import UsernamePasswordToken


app = FastAPI()

# JWT token settings
SECRET_KEY = 'secretSERCRET007'
EXPIRE_MINUTES = 60 * 40
ALGORITHM = "HS256"

# create login manager
auth_manager = AuthManager(
    app=app,
    secret_key=SECRET_KEY,
    algorithm=ALGORITHM,
    expire_minutes=EXPIRE_MINUTES
)

# now you can use login_manager directly or py adding it to the application statement
# it`s comfortable while dealing with APIRouters
app.state.auth_manager = auth_manager


@app.get("/")
@login_required  # make this endpoint allowed only for authenticated users
async def homepage(request: Request):
    current_user = request.user
    return {"current_user": current_user}


@app.post("/auth/token", status_code=201)
async def get_access_token(request: Request, user_data: UsernamePasswordToken = Body()):
    # ... here goes db user verification
    token = request.app.state.auth_manager.create_token(user_data)
    return {"access_token": token}

```

Auth manager adds authentication middleware to your application instance and uses authentication backends to treat token and
request user instance. 
