from typing import Union

from pydantic import BaseModel, EmailStr


#######################################################################
class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    username: str
    surname: str
    type_signup: str = "mailpassword"


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    surname: str
    blocked: str

    class Config:
        orm_mode = True


class DriverInfo(BaseModel):
    ratings: float
    licence_plate: str
    model: str


class UserFullInfo(BaseModel):
    email: EmailStr
    username: str
    surname: str
    blocked: bool
    ratings: float
    driver: Union[DriverInfo, None]

    class Config:
        orm_mode = True


#######################################################################


class WalletWithdrawalSchema(BaseModel):
    user_external_wallet_address: str
    amount_in_ethers: str


#######################################################################


class PassengerAddress(BaseModel):
    street_name: str
    street_number: int


class PassengerSelfProfile(BaseModel):
    email: str
    username: str
    surname: str
    ratings: float
    photo: str


class PassengerProfile(BaseModel):
    username: str
    surname: str
    ratings: float
    photo: str


#######################################################################
class DriverVehicle(BaseModel):
    licence_plate: str
    model: str


class DriverProfile(BaseModel):
    username: str
    surname: str
    ratings: float
    licence_plate: str
    model: str
    photo: str


class DriverSelfProfile(BaseModel):
    email: str
    username: str
    surname: str
    ratings: float
    licence_plate: str
    model: str
    photo: str


#######################################################################
class DriverAvailability(BaseModel):
    email: str
    username: str
    surname: str
    ratings: float
    licence_plate: str
    model: str
    photo: str


#######################################################################
class PassengerRating(BaseModel):
    passenger_email: str
    trip_id: int
    ratings: int
    message: str


class DriverRating(BaseModel):
    driver_email: str
    trip_id: int
    ratings: int
    message: str


#######################################################################
class DriverReport(BaseModel):
    driver_email: str
    trip_id: int
    reason: str


class ReportDelete(BaseModel):
    report_id: int
