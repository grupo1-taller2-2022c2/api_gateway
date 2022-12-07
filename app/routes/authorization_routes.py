import os

from pydantic import EmailStr

from app.schemas.users_schemas import UserSchema
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.auth_schemas import *
from jose import JWTError, jwt
from passlib.context import CryptContext
import requests
from datetime import datetime, timedelta
from typing import Union
import firebase_admin
from firebase_admin import credentials, auth, exceptions
from starlette import status
from app.config.firebase_config import auth_app

router = APIRouter()
url_base = os.getenv("USERS_BASE_URL")

SECRET_KEY = "9830e8615a20b5b145edd6cbf11ca1943cb15dac7ff72be7fd0f046d133b2740"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_google_signin_user(token):
    # auth_app = firebase_admin.getApp(name="authorizationServiceAccount")
    print("The google token is:" + token)
    decoded_token = auth.verify_id_token(token, app=auth_app)
    return decoded_token["email"]


def custom_credentials_exception(message):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_useremail(
    token: str = Depends(oauth2_scheme),
    is_google_token: Union[str, None] = Header(default=None),
):
    try:
        if (
            is_google_token and is_google_token == "true"
        ):  # Se trata de un token de proveedor de identidad federada (Google)
            useremail: EmailStr = validate_google_signin_user(token)
        else:  # Se trata de un token nuestro de email password tradicional
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            useremail: EmailStr = payload.get("sub")
        if useremail is None:
            raise custom_credentials_exception("Could not validate credentials")
    except auth.ExpiredIdTokenError:
        raise custom_credentials_exception("ID token has expired")
    except auth.InvalidIdTokenError:
        raise custom_credentials_exception("ID token is malformed or invalid")
    except exceptions.FirebaseError as ex:
        raise custom_credentials_exception(f"Failed to verify ID token: {ex}")
    except Exception:
        raise custom_credentials_exception("Could not validate credentials")

    if user_is_blocked(useremail):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User blocked by admin",
        )
    return useremail


def user_is_blocked(user_email: EmailStr):
    url = url_base + "/users/blocked/" + user_email
    response = requests.get(url=url).json()
    return response["is_blocked"]


# form_data.username is the email of the user!


@router.post("/token", status_code=status.HTTP_200_OK)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    url = url_base + "/users/grantaccess"

    response = requests.post(
        url=url, json={"email": form_data.username, "password": form_data.password}
    )
    if not response.ok:
        raise HTTPException(
            status_code=response.status_code, detail=response.json()["detail"]
        )

    user: UserSchema = response.json()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
