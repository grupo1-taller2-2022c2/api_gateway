from pydantic import BaseModel, EmailStr


#######################################################################
class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    username: str
    surname: str


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    surname: str

    class Config:
        orm_mode = True


#######################################################################
class PassengerAddress(BaseModel):
    street_name: str
    street_number: int


class PassengerSelfProfile(BaseModel):
    email: str
    username: str
    surname: str
    ratings: float


class PassengerProfile(BaseModel):
    username: str
    surname: str
    ratings: float


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


class DriverSelfProfile(BaseModel):
    email: str
    username: str
    surname: str
    ratings: float
    licence_plate: str
    model: str
