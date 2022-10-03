import json

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import requests
from fastapi.responses import RedirectResponse
from starlette import status

from app.routes.authorization_routes import get_current_user_id
from app.schemas.users_schemas import *

router = APIRouter()

url_base = "http://127.0.0.1:3001/"


@router.post("/users/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def user_signup(user: UserSignUp):
    url = url_base + "users/signup"
    return requests.post(url=url, json=user)


@router.get("/users/", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users():
    url = url_base + "users/"
    """try:
        response = requests.get(url=url)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Gateway Error")"""
    return RedirectResponse(url)


@router.post("/passengers/address", status_code=status.HTTP_200_OK)
def user_add_pred_address(user: PassengerAddress, user_id: int = Depends(get_current_user_id)):
    url = url_base + "passengers/address"
    new_user = {
        "user_id": user_id,
        "street_name": user.street_name,
        "street_number": user.street_number
    }
    return requests.post(url=url, json=json.dump(new_user))


@router.post("/drivers/vehicle", status_code=status.HTTP_200_OK)
def add_vehicle(vehicle: DriverVehicle, user_id: int = Depends(get_current_user_id)):
    url = url_base + "drivers/vehicle"
    new_vehicle = {
        "user_id": user_id,
        "licence_plate": vehicle.licence_plate,
        "model": vehicle.model
    }
    return requests.post(url=url, json=json.dump(new_vehicle))
