from typing import Union

from pydantic import BaseModel, EmailStr


class DriverLocationSchema(BaseModel):
    street_name: str
    street_num: int


class TripState(BaseModel):
    trip_id: int
    status: str


class TripCreate(BaseModel):
    src_address: str
    src_number: int
    dst_address: str
    dst_number: int
    duration: float
    distance: float
    trip_type: Union[str, None]
