from datetime import datetime

from pydantic import BaseModel, Field


class NewTrip(BaseModel):
    checkin_date: int = Field()
    checkout_date: int = Field()
    country: str = Field()
    price: float = Field(ge=0.01, examples=[100.78])
    hotel: str = Field()
    description: str = Field(default="")


class TripId(BaseModel):
    id: int = Field(description='ID of created item')


class CreatedTrip(NewTrip, TripId):
    created_at: datetime
    updated_at: datetime


class DeletedTrip(TripId):
    status: bool = True
