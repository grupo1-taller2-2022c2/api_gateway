import os
from app.schemas.users_schemas import UserSchema
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.auth_schemas import *
from jose import JWTError, jwt
from passlib.context import CryptContext
import requests
from datetime import datetime, timedelta
from typing import Union

from starlette import status

router = APIRouter()
url_base = os.getenv('USERS_BASE_URL')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

#     user = fake_decode_token(token, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
#     if False:  # current_user.disabled:  # TODO: campo disabled todavia no existe
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# # form_data.username is the email of the user!


@router.post("/token",  status_code=status.HTTP_200_OK)
def user_signin(form_data: OAuth2PasswordRequestForm = Depends()):
    url = url_base + "/users/grantaccess"
    try:
        user: UserSchema = requests.post(url=url, json={"email": form_data.username,
                                                        "password": form_data.password}).json()

        print(user)
    except Exception as e:
        raise HTTPException(status_code=403, detail="Failed to sign in")
    # Habilita al usuario en la base de datos
    return {"access_token": user['email'], "token_type": "bearer"}


# @router.get("/me")
# def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
#     return current_user

# SECRET_KEY = "9830e8615a20b5b145edd6cbf11ca1943cb15dac7ff72be7fd0f046d133b2740"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
# def user_signin(form_data: OAuth2PasswordRequestForm = Depends()):
#     url = url_base + "users/signin"
#     # try:
#     user: UserSignIn = requests.post(url=url, json={"email": form_data.username,
#                                                     "password": form_data.password}).json()
#     # except Exception as e:
#     #     raise HTTPException(status_code=403, detail="Failed to sign in")

#     # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # access_token = create_access_token(
#     #     data={"sub": user.user_id}, expires_delta=access_token_expires
#     # )
#     # return {"access_token": access_token, "token_type": "bearer"}
#     return {user: user}


# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user_id(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     return user_id
