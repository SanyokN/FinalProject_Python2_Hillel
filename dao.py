import uuid

from fastapi import HTTPException

from database import Trip, User, session
from utils.utils_hashlib import get_password_hash


def create_trip(
    checkin_day: int,
    checkin_month: int,
    checkin_year: int,
    checkout_day: int,
    checkout_month: int,
    checkout_year: int,
    country: str,
    price: float,
    hotel: str,
    description: str,
    cover_url,
) -> Trip:
    trip = Trip(
        checkin_day=checkin_day,
        checkin_month=checkin_month,
        checkin_year=checkin_year,
        checkout_day=checkout_day,
        checkout_month=checkout_month,
        checkout_year=checkout_year,
        country=country,
        price=price,
        hotel=hotel,
        description=description,
        cover_url=str(cover_url),
    )
    session.add(trip)
    session.commit()
    return trip


def get_all_trips(limit: int, skip: int, name: str | None) -> list[Trip]:
    if name:
        trips = (
            session.query(Trip)
            .filter(Trip.name.icontains(name))
            .limit(limit)
            .offset(skip)
            .all()
        )
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


def create_user(name: str, surname: str, email: str, password: str) -> User:
    user = User(
        name=name,
        surname=surname,
        email=email,
        hashed_password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    return user


def get_user_by_email(email: str) -> User | None:
    user = session.query(User).filter(User.email == email).first()
    return user


def get_user_by_uuid(user_uuid: uuid.UUID) -> User | None:
    user = session.query(User).filter(User.user_uuid == user_uuid).first()
    return user


def activate_user_account(user: User) -> User:
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Already was verified")
    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
