# coding=utf-8

from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic.main import BaseModel


router = APIRouter()

# TODO: There is a bug, if tokenUrl is relative url, it is relative by swagger page url
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "testfakehashed",  # test
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "testfakehashed",  # test
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    disabled: Optional[bool] = None


def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = fake_users_db.get(token)
    if user_data.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return User(**user_data)


@router.get("/shutterisland/", summary="OAuth2 password flow protect")
def shutter_island(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.get("/users/me/", summary="Get current user")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token/", summary="OAuth2 password flow login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if user_dict.get("hashed_password") != form_data.password + "fakehashed":
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_dict.get("username"), "token_type": "bearer"}
