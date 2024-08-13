from fastapi import APIRouter, BackgroundTasks, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import dao
from background_tasks.confirm_registration import confirm_registration
from dao import get_all_trips_dao, get_trip_by_id_dao
from utils.jwt_auth import get_user_web, set_cookies_web

templates = Jinja2Templates(directory="templates")
web_router = APIRouter(prefix="")


@web_router.get("/trip/{trip_id}", include_in_schema=True)
def get_trip_by_id_web(request: Request, trip_id: int, user=Depends(get_user_web)):
    trip = get_trip_by_id_dao(trip_id)
    context = {
        "request": request,
        "trip": trip,
        "title": f"Data on trip to {trip.country} with price {trip.price} $",
        "user": user,
    }
    response = templates.TemplateResponse("details.html", context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.get("/", include_in_schema=True)
@web_router.post("/", include_in_schema=True)
def index(request: Request, user=Depends(get_user_web), query: str = Form(None)):
    context = {
        "request": request,
        "trips": get_all_trips_dao(50, 0, query),
        "title": "Main page",
        "user": user,
    }
    response = templates.TemplateResponse("index.html", context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.get("/register/", include_in_schema=True)
@web_router.post("/register/", include_in_schema=True)
def web_register(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(None),
    surname: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    user=Depends(get_user_web),
):
    if user:
        redirect_url = request.url_for("index")
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response_with_cookies = set_cookies_web(user, response)
        return response_with_cookies
    if request.method == "GET":
        context = {"request": request, "title": "Register"}
        return templates.TemplateResponse("registration.html", context=context)
    maybe_user = dao.get_user_by_email_dao(email)
    context = {
        "request": request,
        "title": "Register",
        "trips": get_all_trips_dao(limit=100, skip=0, name=""),
        "user": maybe_user,
    }
    if not maybe_user:
        created_user = dao.create_user_dao(name, surname, email, password)
        background_tasks.add_task(confirm_registration, created_user, request.base_url)
        context["user"] = created_user
    redirect_url = request.url_for("index")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response_with_cookies = set_cookies_web(context["user"], response)
    return response_with_cookies
