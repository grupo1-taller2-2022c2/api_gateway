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
    print("hola")
    url = url_base + "/users/signup"
    response = requests.post(url=url, json=dict(user)).json()
    print(response)
    return response


@router.get("/users/", response_model=List[UserSchema], status_code=status.HTTP_200_OK)
def get_users():
    url = url_base + "/users/"
    try:
        response = requests.get(url=url).json()
        return response
    except HTTPException as _:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)


@router.post("/passengers/address", status_code=status.HTTP_200_OK)
def user_add_pred_address(user: PassengerAddress, useremail: EmailStr = Depends(get_current_useremail)):
    print("holaa")
    url = url_base + "/passengers/address"
    new_user = {
        "email": useremail,
        "street_name": user.street_name,
        "street_number": user.street_number
    }
    return requests.post(url=url, json=new_user).json()


# @router.post("/drivers/vehicle", status_code=status.HTTP_200_OK)
# def add_vehicle(vehicle: DriverVehicle, user_id: int = Depends(get_current_useremail)):
#     url = url_base + "/drivers/vehicle"
#     new_vehicle = {
#         "user_id": user_id,
#         "licence_plate": vehicle.licence_plate,
#         "model": vehicle.model
#     }
#     return requests.post(url=url, json=json.dump(new_vehicle)).json()
