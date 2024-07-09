import uuid
from datetime import datetime

from sqlalchemy import (UUID, Boolean, Column, DateTime, Float, Integer,
                        Sequence, String, Text, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

import config

Base = declarative_base()


class BaseInfoMixin:
    id = Column(Integer, Sequence("trip_id_seq"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Trip(BaseInfoMixin, Base):
    __tablename__ = "trips"

    checkin_date = Column(Integer, nullable=False)
    checkout_date = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    hotel = Column(Text, nullable=False)
    description = Column(Text)

    def __str__(self):
        return (
            f"<Trip: {self.checkin_date=}; {self.checkout_date=}, "
            f"{self.country=}, {self.price=}, {self.hotel=}>"
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


engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
