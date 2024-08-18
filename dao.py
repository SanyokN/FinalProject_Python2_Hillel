import uuid
from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import OrderTrip, Trip, User, session
from utils.utils_hashlib import get_password_hash


def create_trip_dao(
    checkin_date: date,
    checkout_date: date,
    country: str,
    price: float,
    hotel: str,
    description: str,
    cover_url,
) -> Trip:
    trip = Trip(
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        country=country,
        price=price,
        hotel=hotel,
        description=description,
        cover_url=str(cover_url),
    )
    session.add(trip)
    session.commit()
    return trip


def get_all_trips_dao(limit: int, skip: int, country: str | None) -> list[Trip]:
    if country:
        trips = (
            session.query(Trip)
            .filter(Trip.country.icontains(country))
            .limit(limit)
            .offset(skip)
            .all()
        )
    else:
        trips = session.query(Trip).limit(limit).offset(skip).all()
    return trips


def get_trip_by_id_dao(trip_id) -> Trip | None:
    trip = session.query(Trip).filter(Trip.id == trip_id).first()
    return trip


def update_trip_dao(trip_id: int, trip_data: dict) -> Trip:
    trip_data["cover_url"] = str(trip_data["cover_url"])
    session.query(Trip).filter(Trip.id == trip_id).update(trip_data)
    session.commit()
    trip = session.query(Trip).filter(Trip.id == trip_id).first()
    return trip


def delete_trip_dao(trip_id) -> None:
    session.query(Trip).filter(Trip.id == trip_id).delete()
    session.commit()


def create_user_dao(name: str, surname: str, email: str, password: str) -> User:
    try:
        user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=get_password_hash(password),
        )
        session.add(user)
        session.commit()
        return user
    except Exception:
        session.rollback()


def get_user_by_email_dao(email: str) -> User | None:
    user = session.query(User).filter(User.email == email).first()
    return user


def get_user_by_uuid_dao(user_uuid: uuid.UUID) -> User | None:
    user = session.query(User).filter(User.user_uuid == user_uuid).first()
    return user


def activate_user_account_dao(user: User) -> User:
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Already was verified")
    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_or_create(model, **kwargs):
    query = select(model).filter_by(**kwargs)
    instance = session.execute(query).scalar_one_or_none()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def fetch_order_trips(order_id: int) -> list:
    query = (
        select(OrderTrip)
        .filter(OrderTrip.order_id == order_id)
        .options(joinedload(OrderTrip.trip))
    )
    result = session.execute(query).scalars().all()
    return result
