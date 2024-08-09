from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

import dao
from background_tasks.confirm_registration import confirm_registration
from dao import get_all_trips, get_trip_by_id

templates = Jinja2Templates(directory="templates")
web_router = APIRouter(prefix="")


@web_router.get("/trip/{trip_id}", include_in_schema=True)
def get_trip_by_id_web(request: Request, trip_id: int):
    trip = get_trip_by_id(trip_id)
    context = {
        "request": request,
        "trip": trip,
        "title": f"Data on trip to {trip.country} with price {trip.price} $",
    }
    return templates.TemplateResponse("details.html", context=context)


@web_router.get("/", include_in_schema=True)
@web_router.post("/", include_in_schema=True)
def index(request: Request, query: str = Form(None)):
    context = {
        "request": request,
        "trips": get_all_trips(50, 0, query),
        "title": "Main page",
    }
    return templates.TemplateResponse("index.html", context=context)


@web_router.get("/register/", include_in_schema=True)
@web_router.post("/register/", include_in_schema=True)
def web_register(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(None),
    surname: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
):
    if request.method == "GET":
        context = {"request": request, "title": "Register"}
        return templates.TemplateResponse("registration.html", context=context)
    created_user = dao.create_user(name, surname, email, password)
    background_tasks.add_task(confirm_registration, created_user, request.base_url)
    context = {
        "request": request,
        "title": "Register",
        "trips": get_all_trips(limit=100, skip=0, name=""),
        "user": created_user,
    }
    return templates.TemplateResponse("index.html", context=context)
