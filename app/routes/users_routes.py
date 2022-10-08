import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import requests
from fastapi.responses import RedirectResponse
from starlette import status

from app.routes.authorization_routes import get_current_useremail
from app.schemas.users_schemas import *

router = APIRouter()

url_base = os.getenv('USERS_BASE_URL')


@router.post("/users/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def user_signup(user: UserSignUp):
    url = url_base + "/users/signup"
    response = requests.post(url=url, json=dict(user))
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/users/", response_model=List[UserSchema], status_code=status.HTTP_200_OK)
def get_users():
    url = url_base + "/users/"
    response = requests.post(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.post("/passengers/address", status_code=status.HTTP_200_OK)
def user_add_pred_address(user: PassengerAddress, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/passengers/address"
    new_user = {
        "email": useremail,
        "street_name": user.street_name,
        "street_number": user.street_number
    }
    response = requests.post(url=url, json=new_user)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.post("/drivers/vehicle", status_code=status.HTTP_200_OK)
def add_vehicle(vehicle: DriverVehicle, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/vehicle"
    new_vehicle = {
        "email": useremail,
        "licence_plate": vehicle.licence_plate,
        "model": vehicle.model
    }
    response = requests.post(url=url, json=new_vehicle)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])
