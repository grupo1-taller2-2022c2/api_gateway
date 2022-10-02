from fastapi import APIRouter
from typing import List
import requests

from starlette import status
from app.schemas.users_schemas import *

router = APIRouter()

url_base = ""


@router.post("users/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def user_signup(user: UserSignUp):
    url = url_base + "users/signup"
    return requests.post(url=url, json=user)


@router.get("users/", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users():
    url = url_base + "users/"
    return requests.get(url=url)


@router.post("passengers/address", status_code=status.HTTP_200_OK)
def user_add_pred_address(user: PassengerAddress):
    url = url_base + "passengers/address"
    return requests.post(url=url, json=user)


@router.post("drivers/vehicle", status_code=status.HTTP_200_OK)
def add_vehicle(vehicle: DriverVehicle):
    url = url_base + "drivers/vehicle"
    return requests.post(url=url, json=vehicle)
