import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Union
import requests
from fastapi.responses import RedirectResponse
from starlette import status

from app.routes.authorization_routes import get_current_useremail
from app.schemas.trips_schemas import DriverLocationSchema, TripState, TripCreate, LocationCreate, ExpoToken
from app.schemas.users_schemas import *

router = APIRouter()

url_base = os.getenv('TRIPS_BASE_URL')


@router.post("/drivers/last_location", status_code=status.HTTP_200_OK)
def save_last_location(driver: DriverLocationSchema, useremail: EmailStr = Depends(get_current_useremail)):
    """Save the driver's last location"""
    url = url_base + "/drivers/last_location"
    body = {"email": useremail, "street_name": driver.street_name, "street_num": driver.street_num}
    response = requests.post(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/drivers/last_location/{driver}", status_code=status.HTTP_200_OK)
def gat_drivers_last_location(driver: str, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/last_location/" + driver
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.delete("/drivers/last_location/", status_code=status.HTTP_200_OK)
def delete_drivers_last_location(useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/last_location/"
    body = {"email": useremail}
    response = requests.delete(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/drivers/assigned_trip/", status_code=status.HTTP_200_OK)
def gat_drivers_assigned_trip(useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/assigned_trip/" + useremail
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.post("/trips/", status_code=status.HTTP_201_CREATED)
def create_trip_and_driver_lookup(trip: TripCreate, useremail: EmailStr = Depends(get_current_useremail)):
    """Look for driver once the passenger creates a trip"""
    url = url_base + "/trips/"
    body = {"src_address": trip.src_address,
            "src_number": trip.src_number,
            "dst_address": trip.dst_address,
            "dst_number": trip.dst_number,
            "passenger_email": useremail,
            "duration": trip.duration,
            "distance": trip.distance,
            "trip_type": trip.trip_type}
    response = requests.post(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/trips/cost/", status_code=status.HTTP_200_OK)
def calculate_cost(src_address: str, src_number: int, dst_address: str, dst_number: int, duration: float,
                   distance: float,
                   trip_type: Union[str, None] = None, useremail: EmailStr = Depends(get_current_useremail)):
    """Get the price of the trip"""
    url = url_base + "/trips/cost/"
    response = requests.get(url=url, params={"src_address": src_address, "src_number": src_number,
                                             "dst_address": dst_address, "dst_number": dst_number, "duration": duration,
                                             "distance": distance, "trip_type": trip_type,
                                             "passenger_email": useremail})
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/trips/history/", status_code=status.HTTP_200_OK)
def get_travel_history(user_type: Union[str, None] = None, useremail: EmailStr = Depends(get_current_useremail)):
    """Get the last five travel histories from the passenger.
    If the travel history required is for the driver, request with param 'user_type': 'driver'"""
    url = url_base + "/trips/history/" + useremail
    response = requests.get(url=url, params={"user_type": user_type})
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/trips/{trip_id}", status_code=status.HTTP_200_OK)
def get_trip(trip_id: int):
    """Get info about the trip with the id"""
    url = url_base + "/trips/" + str(trip_id)
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/trips/", status_code=status.HTTP_200_OK)
def change_trip_state(trip: TripState, useremail: EmailStr = Depends(get_current_useremail)):
    """Modify the trip state from the driver. The status can be: Accept, Deny, Initialize, Finalize"""
    url = url_base + "/trips/"
    body = {"trip_id": trip.trip_id, "driver_email": useremail, "status": trip.action}
    response = requests.patch(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.post("/trips/saved_location/", status_code=status.HTTP_201_CREATED)
def add_passenger_saved_location(location: LocationCreate, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/trips/saved_location/"
    body = {"email": useremail, "location": location.location, "street_name": location.street_name, "street_num": location.street_num}
    response = requests.post(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/trips/saved_location/{location_name}", status_code=status.HTTP_200_OK)
def get_passenger_saved_location(location_name: str, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + f"/trips/saved_location/{useremail}/{location_name}"
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/trips/saved_location/", status_code=status.HTTP_200_OK)
def get_all_passenger_saved_location(useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + f"/trips/saved_location/{useremail}"
    response = requests.get(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.post("/notifications/token/", status_code=status.HTTP_201_CREATED)
def save_expo_token(token: ExpoToken, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + f"/notifications/token/"
    body = {"email": useremail, "token": token.token}
    response = requests.post(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.delete("/notifications/token/", status_code=status.HTTP_202_ACCEPTED)
def delete_expo_token(useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + f"/notifications/token/" + useremail
    response = requests.delete(url=url)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])
