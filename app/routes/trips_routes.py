import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Union
import requests
from fastapi.responses import RedirectResponse
from starlette import status

from app.routes.authorization_routes import get_current_useremail
from app.schemas.trips_schemas import DriverLocationSchema, TripState
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


@router.get("/trips/driver_lookup/", status_code=status.HTTP_200_OK)
def look_for_driver(trip_id: int, useremail: EmailStr = Depends(get_current_useremail)):
    """Look for driver once the passenger accepts the price"""
    url = url_base + "/drivers/driver_lookup/"
    response = requests.get(url=url, params={"trip_id": trip_id})
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/trips/cost/", status_code=status.HTTP_200_OK)
def calculate_cost(src_address: str, src_number: int, dst_address: str, dst_number: int,  duration: float, distance: float,
                   trip_type: Union[str, None] = None, useremail: EmailStr = Depends(get_current_useremail)):
    """Get the price of the trip"""
    url = url_base + "/trips/cost/"
    response = requests.get(url=url, params={"src_address": src_address, "src_number": src_number,
                                             "dst_address": dst_address, "dst_number": dst_number, "duration": duration,
                                             "distance": distance, "trip_type": trip_type, "passenger_email": useremail})
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


@router.patch("/trips/accept", status_code=status.HTTP_200_OK)
def accept_trip(trip: TripState, useremail: EmailStr = Depends(get_current_useremail)):
    """Accept the trip from the driver"""
    url = url_base + "/trips/accept"
    body = {"trip_id": trip.trip_id, "driver_email": useremail}
    response = requests.patch(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/trips/deny", status_code=status.HTTP_200_OK)
def deny_trip(trip: TripState, useremail: EmailStr = Depends(get_current_useremail)):
    """Deny the trip from the driver"""
    url = url_base + "/trips/deny"
    body = {"trip_id": trip.trip_id, "driver_email": useremail}
    response = requests.patch(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/trips/initialize", status_code=status.HTTP_200_OK)
def initialize_trip(trip: TripState, useremail: EmailStr = Depends(get_current_useremail)):
    """Initialize the trip from the driver once the driver is in the source address"""
    url = url_base + "/trips/initialize"
    body = {"trip_id": trip.trip_id, "driver_email": useremail}
    response = requests.patch(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.patch("/trips/finalize", status_code=status.HTTP_200_OK)
def finalize_trip(trip: TripState, useremail: EmailStr = Depends(get_current_useremail)):
    """Finalize the trip from the driver once the driver is in the destination address"""
    url = url_base + "/trips/finalize"
    body = {"trip_id": trip.trip_id, "driver_email": useremail}
    response = requests.patch(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])
