# coding=utf-8

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient

router = APIRouter()


def get_user_collection():
    client = MongoClient("mongodb://localhost:27017")
    db = client.get_database("test")
    collection = db.get_collection("fastapi_tutorial_user")
    return collection


class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


class UserIn(User):
    password: str


@router.post("/users/", response_model=User, summary="Write MongoDB")
def create_user(user: UserIn, db=Depends(get_user_collection)):
    user_info = user.dict()
    user_in_db = UserInDB(
        **user_info, hashed_password=user_info["password"] + "fakehash"
    )
    result = db.insert(user_in_db.dict())
    print(result)
    return user_in_db


@router.get("/users/{username}", response_model=User, summary="Read MongoDB")
def get_user(username: str, db=Depends(get_user_collection)):
    result = db.find_one({"username": username})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return result
