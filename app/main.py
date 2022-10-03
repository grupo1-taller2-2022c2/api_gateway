from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users_routes, authorization_routes

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


# app.include_router(users_routes.router, tags=["Users BE"])
app.include_router(authorization_routes.router, tags=["Auth"])
