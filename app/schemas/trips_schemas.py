from pydantic import BaseModel, EmailStr


class DriverLocationSchema(BaseModel):
    street_name: str
    street_num: int


class TripState(BaseModel):
    trip_id: int
