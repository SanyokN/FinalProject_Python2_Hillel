import uuid
from datetime import datetime

from sqlalchemy import (UUID, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Integer, Sequence, String, Text,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import config

Base = declarative_base()


class BaseInfoMixin:
    id = Column(Integer, Sequence("trip_id_seq"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Trip(BaseInfoMixin, Base):
    __tablename__ = "trips"

    checkin_date = Column(Date, nullable=False)
    checkout_date = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    hotel = Column(Text, nullable=False)
    description = Column(Text)
    cover_url = Column(Text, nullable=False)
    trips = relationship("OrderTrip", back_populates="trip")

    def __str__(self):
        return (
            f"<Trip: {self.id=}, {self.checkin_date=} - {self.checkout_date=}, "
            f"{self.country=}, {self.price=} $, {self.hotel=}>"
        )

    __repr__ = __str__


class User(BaseInfoMixin, Base):
    __tablename__ = "users"

    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    user_uuid = Column(UUID, default=uuid.uuid4)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    def __str__(self):
        return f"<User: {self.id=}; {self.name=}, {self.surname=}>"

    __repr__ = __str__


class Order(BaseInfoMixin, Base):
    __tablename__ = "orders"
    user_id = Column(ForeignKey("users.id"), nullable=False)
    is_closed = Column(Boolean, default=False)

    def __str__(self):
        return f"<Order: {self.id=}; {self.user_id=}; {self.is_closed=}>"

    __repr__ = __str__


class OrderTrip(BaseInfoMixin, Base):
    __tablename__ = "order_trips"
    order_id = Column(ForeignKey("orders.id"), nullable=False)
    trip_id = Column(ForeignKey("trips.id"), nullable=False)
    price = Column(Float, nullable=False, default=10.0)
    adults_quantity = Column(Integer, nullable=False, default=1)
    children_quantity = Column(Integer, nullable=False, default=0)
    trip = relationship("Trip", back_populates="trips")

    @property
    def cost(self):
        return self.price * (self.adults_quantity + self.children_quantity / 2)

    def __str__(self):
        return (
            f"<OrderTrip: {self.id=}; {self.order_id=}; {self.adults_quantity=}; "
            f"{self.children_quantity=}; {self.price=}, cost={self.cost}>"
        )

    __repr__ = __str__


engine = create_engine(config.DB_PATH, echo=config.DEBUG)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
