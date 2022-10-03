from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    username: str
    surname: str


class User(BaseModel):
    email: EmailStr
    password: str
    username: str
    surname: str

    class Config:
        orm_mode = True


class PassengerAddress(BaseModel):
    token: str
    street_name: str
    street_number: int


class DriverVehicle(BaseModel):
    token: str
    licence_plate: str
    model: str

