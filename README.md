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
You can you it with JWT-token (default in you headers).

```python
from fastapi import FastAPI, Request, Body

from fastapi_authtools import AuthManager, login_required
from fastapi_authtools.models import UsernamePasswordToken, UserModel


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
    # ... here goes db user verification and getting user information
    # user = get_login_user(user_data)
    user = UserModel(
        email="suslanchikmol@gmail.con",
        username="michael7nightingale"
    )
    token = request.app.state.auth_manager.create_token(user)
    return {"access_token": token}

```

But you can still use cookies to save token, just define `user_cookies` as True when initialize AuthManager.

To use templates and form data you should install `jinja2` and `python-multipart`. 
```python
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi_authtools import AuthManager, login_required
from fastapi_authtools.models import UserModel


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# JWT token settings
SECRET_KEY = 'secretSERCRET007'
EXPIRE_MINUTES = 60 * 40
ALGORITHM = "HS256"

# create login manager
auth_manager = AuthManager(
    app=app,
    use_cookies=True,
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
    return templates.TemplateResponse(
        name="homepage.html",
        context={"request": request, "current_user": request.user}
    )


@app.get('/login')
async def login_get(request: Request):
    return templates.TemplateResponse(
        name='login.html',
        context={"request": request}
    )


@app.post("/login", status_code=201)
async def login_post(request: Request):
    user_data = await request.form()
    # ... here goes db user verification and getting user information
    # user = get_login_user(user_data)
    user = UserModel(
        email="suslanchikmol@gmail.con",
        username="michael7nightingale"
    )
    response = RedirectResponse(app.url_path_for("homepage"), status_code=303)
    app.state.auth_manager.login(response, user)
    return response
```


Auth manager adds authentication middleware to your application instance and uses authentication backends to treat token and
request user instance. 
