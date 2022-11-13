import json
import os

from fastapi import APIRouter, Depends, HTTPException, status, File
from typing import List
import requests
from fastapi.responses import RedirectResponse
from starlette import status

from app.routes.authorization_routes import get_current_useremail
from app.schemas.users_schemas import *

router = APIRouter()

url_base = os.getenv('USERS_BASE_URL')


###############################################################################################
# USERS
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
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


###############################################################################################
# USERS WALLETS
@router.get("/users/{useremail}/wallet", status_code=status.HTTP_200_OK)
def get_user_wallet(useremail: str):
    url = url_base + "/users/" + useremail + "/wallet"
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])

###############################################################################################
# COMPLETE DATA


@router.post("/passengers/address", status_code=status.HTTP_201_CREATED)
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


@router.post("/drivers/vehicle", status_code=status.HTTP_201_CREATED)
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


###############################################################################################
# PASSENGERS PROFILE
@router.get("/passengers/{useremail}", response_model=PassengerProfile, status_code=status.HTTP_200_OK)
def user_profile(useremail: str):
    url = url_base + "/passengers/" + useremail
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/passengers/me/", response_model=PassengerSelfProfile, status_code=status.HTTP_200_OK)
def user_profile(useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/passengers/me/" + useremail
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/passengers/", status_code=status.HTTP_200_OK)
def update_passenger_profile(new_profile: PassengerProfile, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/passengers/" + useremail
    response = requests.patch(url=url, json=dict(new_profile))
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/passengers/picture", status_code=status.HTTP_200_OK)
def update_passenger_picture(photo: bytes = File(default=None), useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/passengers/picture/" + useremail
    response = requests.patch(url=url, data=photo)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


###############################################################################################
# DRIVERS PROFILE
@router.get("/drivers/{useremail}", response_model=DriverProfile, status_code=status.HTTP_200_OK)
def user_profile(useremail: str):
    url = url_base + "/drivers/" + useremail
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/drivers/me/", response_model=DriverSelfProfile, status_code=status.HTTP_200_OK)
def user_profile(useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/me/" + useremail
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/drivers/", status_code=status.HTTP_200_OK)
def update_passenger_profile(new_profile: DriverProfile, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/" + useremail
    response = requests.patch(url=url, json=dict(new_profile))
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/drivers/picture", status_code=status.HTTP_200_OK)
def update_passenger_picture(photo: bytes = File(default=None), useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/picture/" + useremail
    response = requests.patch(url=url, data=photo)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


###############################################################################################
# DRIVERS GET AVAILABLES
@router.get("/drivers/all_available/", response_model=List[DriverAvailability], status_code=status.HTTP_200_OK)
def get_available_drivers():
    url = url_base + "/drivers/all_available/"
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


###############################################################################################
# PASSENGERS RATINGS
@router.post("/passengers/ratings", status_code=status.HTTP_201_CREATED)
def user_add_passenger_ratings(rating: PassengerRating, useremail: EmailStr = Depends(get_current_useremail)):
    """Add a rating to the passenger"""
    url = url_base + "/passengers/ratings"
    response = requests.post(url=url, json=dict(rating))
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/passengers/ratings/all/{passenger_email}", status_code=status.HTTP_200_OK)
def user_get_passenger_ratings(passenger_email: str):
    """Get all ratings about a passenger"""
    url = url_base + "/passengers/ratings/all/" + passenger_email
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/passengers/ratings/{ratings_id}", status_code=status.HTTP_200_OK)
def user_get_passenger_rating(ratings_id: int):
    """Get one rating with rating_id"""
    url = url_base + "/passengers/ratings/" + str(ratings_id)
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


###############################################################################################
# DRIVERS RATINGS
@router.post("/drivers/ratings", status_code=status.HTTP_201_CREATED)
def user_add_driver_ratings(rating: DriverRating, useremail: EmailStr = Depends(get_current_useremail)):
    """Add a rating to the driver"""
    url = url_base + "/drivers/ratings"
    response = requests.post(url=url, json=dict(rating))
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/drivers/ratings/all/{driver_email}", status_code=status.HTTP_200_OK)
def user_get_driver_ratings(driver_email: str):
    """Get all ratings about a driver"""
    url = url_base + "/drivers/ratings/all/" + driver_email
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/drivers/ratings/{ratings_id}", status_code=status.HTTP_200_OK)
def user_get_driver_rating(ratings_id: int):
    """Get one rating with rating_id"""
    url = url_base + "/drivers/ratings/" + str(ratings_id)
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


###############################################################################################
# DRIVER REPORT
@router.post("/drivers/reports", status_code=status.HTTP_201_CREATED)
def report_driver(report: DriverReport, useremail: EmailStr = Depends(get_current_useremail)):
    body = {"driver_email": report.driver_email, "passenger_email": useremail,
            "trip_id": report.trip_id, "reason": report.reason}
    url = url_base + "/drivers/reports"
    response = requests.post(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.delete("/drivers/reports", status_code=status.HTTP_200_OK)
def delete_report_with_report_id(report: ReportDelete):
    url = url_base + "/drivers/reports"
    response = requests.delete(url=url, json=dict(report))
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/drivers/reports/all", status_code=status.HTTP_200_OK)
def get_drivers_reports():
    url = url_base + "/drivers/reports/all"
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])
