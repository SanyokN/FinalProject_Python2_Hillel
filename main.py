from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.templating import Jinja2Templates
from starlette import status

import config
import dao
from api_router.api_users import api_router_users
from database import create_tables
from api_router.schemas_trips import CreatedTrip, DeletedTrip, NewTrip

templates = Jinja2Templates(directory="templates")


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    debug=config.DEBUG,
    lifespan=lifespan,
)


@app.post(
    "/api/trips/create/", status_code=status.HTTP_201_CREATED, tags=["API", "Trips"]
)
def create_trip(new_trip: NewTrip) -> CreatedTrip:
    created_trip = dao.create_trip(**new_trip.model_dump())
    return created_trip


@app.get("/api/trips/", tags=["API", "Trips"])
def get_trips(
    limit: int = Query(default=5, gt=0, le=50, description="Number of trips"),
    skip: int = Query(default=0, ge=0, description="How many to skip"),
    name: str = Query(default="", description="Part of the trip name"),
) -> list[CreatedTrip]:
    trips = dao.get_all_trips(limit=limit, skip=skip, name=name)
    return trips


@app.get("/api/trips/{trip_id}", tags=["API", "Trips"])
def get_trip(
    trip_id: int = Path(gt=0, description="ID of the trip"),
) -> CreatedTrip:
    trip = dao.get_trip_by_id(trip_id=trip_id)
    if trip:
        return trip
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@app.put("/api/trips/{trip_id}", tags=["API", "Trips"])
def update_trip(
    updated_trip: NewTrip,
    trip_id: int = Path(gt=0, description="ID of the trip"),
) -> CreatedTrip:
    trip = dao.get_trip_by_id(trip_id=trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    trip = dao.update_trip(trip_id, updated_trip.model_dump())
    return trip


@app.delete("/api/trips/{trip_id}", tags=["API", "Trips"])
def delete_trip(
    trip_id: int = Path(gt=0, description="ID of the trip"),
) -> DeletedTrip:
    trip = dao.get_trip_by_id(trip_id=trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    dao.delete_trip(trip_id=trip_id)
    return DeletedTrip(id=trip_id)


@app.get("/", include_in_schema=False)
def index_web(request: Request):

    return templates.TemplateResponse(
        "index.html", {"request": request, "": {}, "title": "Main page"}
    )


app.include_router(api_router_users)
