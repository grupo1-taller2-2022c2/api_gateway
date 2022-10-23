import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import requests
from fastapi.responses import RedirectResponse
from starlette import status

from app.routes.authorization_routes import get_current_useremail
from app.schemas.trips_schemas import DriverLocationSchema
from app.schemas.users_schemas import *

router = APIRouter()

url_base = os.getenv('TRIPS_BASE_URL')


@router.post("/drivers/last_location", status_code=status.HTTP_200_OK)
def save_last_location(driver: DriverLocationSchema, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/last_location"
    body = {"email": useremail, "street_name": driver.street_name, "street_num": driver.street_num}
    response = requests.post(url=url, json=body)
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])


@router.get("/drivers/driver_lookup/", status_code=status.HTTP_200_OK)
def look_for_driver(src_address: str, src_number: int, useremail: EmailStr = Depends(get_current_useremail)):
    url = url_base + "/drivers/driver_lookup/"
    response = requests.get(url=url, params={"src_address": src_address, "src_number": src_number})
    if response.ok:
        return response.json()
    raise HTTPException(status_code=response.status_code,
                        detail=response.json()['detail'])
