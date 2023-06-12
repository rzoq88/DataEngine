import json
import pathlib
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from cassandra.cqlengine.management import sync_table
from pydantic.error_wrappers import ValidationError
from . import config, db, utils

from .indexing.client import (
    update_index,
    search_index,
    search_index_add
)

from .shortcuts import redirect, render
from .users.backends import JWTCookieBackend
from .users.decorators import login_required
from .users.models import User
from .users.schemas import (
    UserLoginSchema,
    UserSignupSchema
)
from .data.models import Data
from .data.routers import router as data_router



DB_SESSION = None
BASE_DIR = pathlib.Path(__file__).resolve().parent # app/

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(data_router)


from .handlers import * # noqa


@app.on_event("startup")
def on_startup():
    # triggered when fastapi starts
    print("hello world")
    global DB_SESSION
    DB_SESSION = db.get_session()

    sync_table(User)
    sync_table(Data)
    # session.execute("CREATE KEYSPACE IF NOT EXISTS dataEngine WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };")
    # "CREATE CUSTOM INDEX  fn_prefix ON cyclist_name (firstname) USING 'org.apache.cassandra.index.sasi.SASIIndex';"
    try:
        DB_SESSION.execute('DESC INDEX dataengine.fn_prefix;')
        DB_SESSION.execute('DESC INDEX dataengine.fn_prefix;')
        print('index here')
    except:
        print('creating index')
        DB_SESSION.execute("CREATE CUSTOM INDEX  fn_prefix ON dataengine.Data (email) USING 'org.apache.cassandra.index.sasi.SASIIndex'  WITH OPTIONS = { 'mode' : 'CONTAINS'};")
        DB_SESSION.execute("CREATE CUSTOM INDEX  pw_fn_prefix ON dataengine.Data (password) USING 'org.apache.cassandra.index.sasi.SASIIndex'  WITH OPTIONS = { 'mode' : 'CONTAINS'};")



@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {}, status_code=200)
    return render(request, "home.html", {})


@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request):
    """
    hello world
    """
    context = {}
    return render(request, "account.html", context)

@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    return render(request, "auth/login.html", {})


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, 
    email: str=Form(...), 
    password: str = Form(...),
    next: Optional[str] = "/"
    ):

    raw_data  = {
        "email": email,
        "password": password,
       
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
                "data": data,
                "errors": errors,
            }
    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)
    if "http://127.0.0.1" not in next:
        next = '/'
    return redirect(next, cookies=data)


@app.get("/logout", response_class=HTMLResponse)
def logout_get_view(request: Request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, "auth/logout.html", {})

@app.post("/logout", response_class=HTMLResponse)
def logout_post_view(request: Request):
    return redirect("/login", remove_session=True)

@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "auth/signup.html")


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request, 
    email: str=Form(...), 
    password: str = Form(...),
    password_confirm: str = Form(...)
    ):
    raw_data  = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    User.create_user(email,password)
    if len(errors) > 0:
        return render(request, "auth/signup.html", status_code=400)
    return redirect("/login")


@app.post('/update-index', response_class=HTMLResponse)
def htmx_update_index_view(request:Request):
    count = update_index()
    return HTMLResponse(f"({count}) Refreshed")


@app.get("/search", response_class=HTMLResponse)
def search_detail_view(request:Request, q:Optional[str] = None):
    query = None
    context = {}
    if q is not None:
        query = q
        results = search_index(query)
        num = len(results)
        print(f'here is the results of search {results}')
        # hits = results.get('hits') or []
        # num_hits = results.get('nbHits')
        context = {
            "query": query,
            # "hits": hits,
            "num_hits": num,
            'hits':results
        }
        
    return render(request, "search/detail.html", context)


@app.get("/search/add", response_class=HTMLResponse)
def search_detail_view(request:Request, q1:Optional[str] = None,q3:Optional[str] = None,q2:Optional[str] = None):
    query = None
    context = {}

    if q1 is not None:
        query = [q1,q2,q3]
        results = search_index_add(query)
        print(results)
        num = len(results)
        # print(f'here is the results of search {results}')
        # hits = results.get('hits') or []
        # num_hits = results.get('nbHits')

        context = {
            "query": query,
            # "hits": hits,
            "num_hits": num,
            'hits':results
        }
        
    return render(request, "search/detail.html", context)
