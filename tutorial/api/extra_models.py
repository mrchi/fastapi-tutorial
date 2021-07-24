# coding=utf-8

from typing import Optional, Union
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr


router = APIRouter()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    fullname: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserDB(UserBase):
    hashed_password: str


class UserOut(UserBase):
    pass


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"
    speed: str


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {
        "description": "This is a car",
        "type": "car",
        "speed": "low",
    },
    "item2": {
        "description": "This is a plane",
        "type": "plane",
        "size": 5,
    },
}


@router.post("/thetwotower", response_model=UserOut, summary="Multiple models")
def the_two_tower(user: UserIn):
    user_saved = UserDB(**user.dict(), hashed_password=user.password + "secret")
    return user_saved


@router.get(
    "/theromanholiday",
    response_model=Union[CarItem, PlaneItem],
    summary="Declare multiple types reponse",
)
def the_roman_holiday(item_id: str):
    return items.get(item_id)


@router.get(
    "/catchmeifyoucan",
    response_model=dict[str, float],
    summary="Arbitrary dict response",
)
def catch_me_if_you_can():
    return {"foo": 12.3, "bar": 33.4}
