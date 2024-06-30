from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, String, Text, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import config

Base = declarative_base()


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, Sequence('trip_id_seq'), primary_key=True)
    checkin_date = Column(Integer, nullable=False)
    checkout_date = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    hotel = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return (f'<Trip: {self.checkin_date}; {self.checkout_date}, '
                f'{self.country}, {self.price}, {self.hotel}>')

    __repr__ = __str__


engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
