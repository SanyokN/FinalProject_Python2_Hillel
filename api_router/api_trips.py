from fastapi import Query, Path, HTTPException, APIRouter
from starlette import status

import dao
from api_router.schemas_trips import NewTrip, CreatedTrip, DeletedTrip


api_router_trips = APIRouter(
    prefix='/api/trips',
    tags=['API', 'Trips']
)


@api_router_trips.post('/create/', status_code=status.HTTP_201_CREATED)
def create_trip(new_trip: NewTrip) -> CreatedTrip:
    created_trip = dao.create_trip(**new_trip.model_dump())
    return created_trip


@api_router_trips.get('/')
def get_trips(
        limit: int = Query(default=5, gt=0, le=50, description='Number of trips'),
        skip: int = Query(default=0, ge=0, description='How many to skip'),
        name: str = Query(default='', description='Part of the trip name'),
) -> list[CreatedTrip]:
    trips = dao.get_all_trips(limit=limit, skip=skip, name=name)
    return trips


@api_router_trips.get('/{trip_id}')
def get_trip(
        trip_id: int = Path(gt=0, description='ID of the trip'),
) -> CreatedTrip:
    trip = dao.get_trip_by_id(trip_id=trip_id)
    if trip:
        return trip
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')


@api_router_trips.put('/{trip_id}')
def update_trip(
        updated_trip: NewTrip,
        trip_id: int = Path(gt=0, description='ID of the trip'),
) -> CreatedTrip:
    trip = dao.get_trip_by_id(trip_id=trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    trip = dao.update_trip(trip_id, updated_trip.model_dump())
    return trip


@api_router_trips.delete('/{trip_id}')
def delete_trip(
        trip_id: int = Path(gt=0, description='ID of the trip'),
) -> DeletedTrip:
    trip = dao.get_trip_by_id(trip_id=trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    dao.delete_trip(trip_id=trip_id)
    return DeletedTrip(id=trip_id)
