from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from dao import get_all_trips, get_trip_by_id

templates = Jinja2Templates(directory="templates")
web_router = APIRouter(prefix="")




@web_router.get('/trip/{trip_id}', include_in_schema=True)
def get_trip_by_id_web(request: Request, trip_id: int):
    trip = get_trip_by_id(trip_id)
    context = {
        'request': request,
        'trip': trip,
        'title': f'Data on trip to {trip.country} with price {trip.price} $'
    }
    return templates.TemplateResponse('details.html', context=context)
@web_router.get("/", include_in_schema=True)
@web_router.post('/', include_in_schema=True)
def index(request: Request, query: str = Form(None)):
    context = {
        "request": request,
        "trips": get_all_trips(50, 0, query),
        "title": "Main page",
    }
    return templates.TemplateResponse("index.html", context=context)
