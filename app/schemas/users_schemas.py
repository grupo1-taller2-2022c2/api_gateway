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
    email: EmailStr
    street_name: str
    street_number: int


class DriverVehicle(BaseModel):
    email: EmailStr
    licence_plate: str
    model: str

