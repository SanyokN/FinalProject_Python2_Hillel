from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class NewTrip(BaseModel):
    checkin_day: int = Field()
    checkin_month: int = Field()
    checkin_year: int = Field()
    checkout_day: int = Field()
    checkout_month: int = Field()
    checkout_year: int = Field()
    country: str = Field()
    price: float = Field(ge=0.01, examples=[100.78])
    hotel: str = Field()
    description: str = Field(default="")
    cover_url: HttpUrl


class TripId(BaseModel):
    id: int = Field(description="ID of created item")


class CreatedTrip(NewTrip, TripId):
    created_at: datetime
    updated_at: datetime


class DeletedTrip(TripId):
    status: bool = True
