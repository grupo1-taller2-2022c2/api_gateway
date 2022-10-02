from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSignIn:
    user_id: int
