import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users_routes, authorization_routes, trips_routes
from starlette import status
import requests

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to API Gateway"}


app.include_router(users_routes.router, tags=["Users BE"])
app.include_router(authorization_routes.router, tags=["Auth"])
app.include_router(trips_routes.router, tags=["Trips"])

ENABLE_RESET = (os.getenv('ENABLE_RESET', 'False') == 'True')

if ENABLE_RESET:
    @app.delete("/reset_db", status_code=status.HTTP_200_OK)
    def reset_database():
        users_base_url = os.getenv('USERS_BASE_URL')
        wallets_url_base = os.getenv('WALLETS_BASE_URL')
        trips_url_base = os.getenv('TRIPS_BASE_URL')

        url = users_base_url + "/reset_db"
        requests.delete(url=url)

        url = wallets_url_base + "/reset_db"
        requests.delete(url=url)

        url = trips_url_base + "/reset_db"
        requests.delete(url=url)

        return "Successfully reset"
