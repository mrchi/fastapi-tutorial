# coding=utf-8

from typing import Optional
from fastapi import APIRouter
from fastapi.params import Body
from pydantic import BaseModel, EmailStr

router = APIRouter()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    fullname: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    fullname: Optional[str] = None


@router.post("/12angrymen", response_model=Item, summary="Response model")
def twelve_angry_men(item: Item):
    return item


@router.post(
    "/users",
    response_model=UserOut,
    summary="Different individual request model and response model",
)
def create_user(user: UserIn):
    return user


@router.post(
    "/devils",
    response_model=Item,
    response_model_exclude_unset=True,
    summary="response_model_exclude_unset",
)
def devils(item: Item = Body(..., example={"name": "Tank", "price": 40.0})):
    return item


@router.post(
    "/dahuaxiyou",
    response_model=Item,
    response_model_exclude_defaults=True,
    summary="response_model_exclude_defaults",
)
def dahuaxiyou(
    item: Item = Body(..., example={"name": "Tank", "price": 40.0, "tax": 10.5})
):
    return item


@router.post(
    "/castleinthesky",
    response_model=Item,
    response_model_exclude_none=True,
    summary="response_model_exclude_none",
)
def castleinthesky(item: Item = Body(..., example={"name": "Tank", "price": 40.0})):
    return item


@router.post(
    "/paradiso",
    response_model=Item,
    response_model_exclude={"price", "name"},
    summary="response_model_exclude",
)
def paradiso(item: Item = Body(..., example={"name": "Tank", "price": 40.0})):
    return item


@router.post(
    "/scentofawomen",
    response_model=Item,
    response_model_include={"tags"},
    summary="response_model_include",
)
def scentofawomen(item: Item = Body(..., example={"name": "Tank", "price": 40.0})):
    return item
