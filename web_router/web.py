from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import dao
from background_tasks.confirm_registration import confirm_registration
from dao import get_all_trips_dao, get_trip_by_id_dao
from database import Order, OrderTrip, session
from utils.jwt_auth import get_user_web, set_cookies_web
from utils.utils_hashlib import verify_password

templates = Jinja2Templates(directory="templates")
web_router = APIRouter(prefix="")


@web_router.post("/quantity-adult-decrease")
def quantity_adult_decrease(
    request: Request, trip_id: int = Form(), user=Depends(get_user_web)
):
    trip = dao.get_trip_by_id_dao(trip_id)
    if not all([user, trip]):
        context = {
            "request": request,
            "trips": get_all_trips_dao(50, 0, ""),
            "title": "Main page",
            "user": user,
        }
        return templates.TemplateResponse("index.html", context=context)
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    order_trip: OrderTrip = dao.get_or_create(
        OrderTrip, order_id=order.id, trip_id=trip_id
    )
    if order_trip.adults_quantity > 1:
        order_trip.adults_quantity -= 1
        session.add(order_trip)
        session.commit()
        session.refresh(order_trip)
    redirect_url = request.url_for("get_cart")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response


@web_router.post("/quantity-adult-increase")
def quantity_adult_increase(
    request: Request, trip_id: int = Form(), user=Depends(get_user_web)
):
    trip = dao.get_trip_by_id_dao(trip_id)
    if not all([user, trip]):
        context = {
            "request": request,
            "trips": get_all_trips_dao(50, 0, ""),
            "title": "Main page",
            "user": user,
        }
        return templates.TemplateResponse("index.html", context=context)
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    order_trip: OrderTrip = dao.get_or_create(
        OrderTrip, order_id=order.id, trip_id=trip_id
    )
    order_trip.adults_quantity += 1
    session.add(order_trip)
    session.commit()
    session.refresh(order_trip)
    redirect_url = request.url_for("get_cart")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response


@web_router.post("/quantity-children-decrease")
def quantity_children_decrease(
    request: Request, trip_id: int = Form(), user=Depends(get_user_web)
):
    trip = dao.get_trip_by_id_dao(trip_id)
    if not all([user, trip]):
        context = {
            "request": request,
            "trips": get_all_trips_dao(50, 0, ""),
            "title": "Main page",
            "user": user,
        }
        return templates.TemplateResponse("index.html", context=context)
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    order_trip: OrderTrip = dao.get_or_create(
        OrderTrip, order_id=order.id, trip_id=trip_id
    )
    if order_trip.children_quantity > 0:
        order_trip.children_quantity -= 1
        session.add(order_trip)
        session.commit()
        session.refresh(order_trip)
    redirect_url = request.url_for("get_cart")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response


@web_router.post("/quantity-children-increase")
def quantity_children_increase(
    request: Request, trip_id: int = Form(), user=Depends(get_user_web)
):
    trip = dao.get_trip_by_id_dao(trip_id)
    if not all([user, trip]):
        context = {
            "request": request,
            "trips": get_all_trips_dao(50, 0, ""),
            "title": "Main page",
            "user": user,
        }
        return templates.TemplateResponse("index.html", context=context)
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    order_trip: OrderTrip = dao.get_or_create(
        OrderTrip, order_id=order.id, trip_id=trip_id
    )
    order_trip.children_quantity += 1
    session.add(order_trip)
    session.commit()
    session.refresh(order_trip)
    redirect_url = request.url_for("get_cart")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response


@web_router.post("/delete-people-quantity")
def delete_people_quantity(
    request: Request, trip_id: int = Form(), user=Depends(get_user_web)
):
    trip = dao.get_trip_by_id_dao(trip_id)
    if not all([user, trip]):
        context = {
            "request": request,
            "trips": get_all_trips_dao(50, 0, ""),
            "title": "Main page",
            "user": user,
        }
        return templates.TemplateResponse("index.html", context=context)
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    order_trip: OrderTrip = dao.get_or_create(
        OrderTrip, order_id=order.id, trip_id=trip_id
    )
    order_trip.adults_quantity, order_trip.children_quantity = 0, 0
    session.add(order_trip)
    session.commit()
    session.refresh(order_trip)
    redirect_url = request.url_for("get_cart")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response


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


@web_router.get("/cart", include_in_schema=True)
def get_cart(request: Request, user=Depends(get_user_web)):
    if not user:
        context = {
            "request": request,
            "trips": get_all_trips_dao(50, 0, ""),
            "title": "Main page",
        }
        return templates.TemplateResponse("index.html", context=context)
    order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    cart = dao.fetch_order_trips(order.id)
    context = {"request": request, "cart": cart, "title": "Cart", "user": user}
    response = templates.TemplateResponse("cart.html", context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.get("/", include_in_schema=True)
@web_router.post("/", include_in_schema=True)
def index(
    request: Request,
    user=Depends(get_user_web),
    country: str = Form(None),
    price: int | float = Form(None),
    checkin_date_from: date = Form(None),
    checkin_date_to: date = Form(None),
):
    context = {
        "request": request,
        "trips": get_all_trips_dao(
            50, 0, country, price, checkin_date_from, checkin_date_to
        ),
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
        "trips": get_all_trips_dao(
            limit=100,
            skip=0,
            country="",
            price=None,
            checkin_date_from=date.today(),
            checkin_date_to=None,
        ),
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


@web_router.get("/login/", include_in_schema=True)
@web_router.post("/login/", include_in_schema=True)
def web_login(
    request: Request,
    email: str = Form(None),
    password: str = Form(None),
    user=Depends(get_user_web),
):
    if user:
        redirect_url = request.url_for("index")
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response_with_cookies = set_cookies_web(user, response)
        return response_with_cookies
    context = {"request": request}
    if request.method == "GET":
        context["title"] = "Login"
        return templates.TemplateResponse("login.html", context=context)
    maybe_user = dao.get_user_by_email_dao(email)
    if not maybe_user:
        context["title"] = "Login"
        context["error"] = True
        context["email_value"] = email
        return templates.TemplateResponse("login.html", context=context)
    if verify_password(password, maybe_user.hashed_password):
        context = {
            "title": "Login",
            "trips": get_all_trips_dao(
                limit=100,
                skip=0,
                country="",
                price=None,
                checkin_date_from=date.today(),
                checkin_date_to=None,
            ),
            "user": maybe_user,
            **context,
        }
        response = templates.TemplateResponse("index.html", context=context)
        response_with_cookies = set_cookies_web(user, response)
        return response_with_cookies
    context["title"] = "Login"
    context["error"] = True
    context["email_value"] = email
    return templates.TemplateResponse("login.html", context=context)


@web_router.get("/logout/", include_in_schema=True)
def web_logout(request: Request):
    context = {
        "request": request,
        "trips": get_all_trips_dao(50, 0, "", None, date.today(), None),
        "title": "Main page",
        "user": None,
    }
    response = templates.TemplateResponse("index.html", context=context)
    response.delete_cookie(key="token_user_usanka")
    return response


@web_router.post("/add-trip-to-cart/", name="add_trip_to_cart")
def add_trip_to_cart(
    request: Request, trip_id: int = Form(), user=Depends(get_user_web)
):
    trip = dao.get_trip_by_id_dao(trip_id)
    if not all([user, trip]):
        context = {
            "request": request,
            "trips": get_all_trips_dao(50, 0, ""),
            "title": "Main page",
        }
        return templates.TemplateResponse("index.html", context=context)
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    order_trip: OrderTrip = dao.get_or_create(
        OrderTrip, order_id=order.id, trip_id=trip_id
    )
    order_trip.price = trip.price
    session.add(order_trip)
    session.commit()
    session.refresh(order_trip)
    redirect_url = request.url_for("index")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.get("/search/")
def search(request: Request, user=Depends(get_user_web)):
    context = {
        "request": request,
        "trips": get_all_trips_dao(50, 0, "", None, date.today(), None),
        "title": "Search for trips",
        "user": user,
    }
    response = templates.TemplateResponse("search.html", context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies
