from database import Trip, session


def create_trip(customer_name: str,
                checkin_date: int,
                checkout_date: int,
                country: str,
                price: float,
                hotel: str,
                notes: str | None) -> Trip:
    trip = Trip(
        customer_name=customer_name,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        country=country,
        price=price,
        hotel=hotel,
        notes=notes
    )
    session.add(trip)
    session.commit()
    return trip


def get_all_trips(limit: int, skip: int, name: str) -> list[Trip]:
    if name:
        trips = session.query(Trip).filter(Trip.name.icontains(name)).limit(limit).offset(skip).all()
    else:
        trips = session.query(Trip).limit(limit).offset(skip).all()
    return trips


def get_trip_by_id(trip_id) -> Trip | None:
    trip = session.query(Trip).filter(Trip.id == trip_id).first()
    return trip


def update_trip(trip_id: int, trip_data: dict) -> Trip:
    session.query(Trip).filter(Trip.id == trip_id).update(trip_data)
    session.commit()
    trip = session.query(Trip).filter(Trip.id == trip_id).first()
    return trip


def delete_trip(trip_id) -> None:
    session.query(Trip).filter(Trip.id == trip_id).delete()
    session.commit()
