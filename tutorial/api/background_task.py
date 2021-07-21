# coding=utf-8

from fastapi import APIRouter, BackgroundTasks
from fastapi.param_functions import Depends
from pydantic import EmailStr

router = APIRouter()


def fake_send_email(email: EmailStr, content: str):
    print(f"send content [{content}] to email [{email}].")


def fake_send_register_mail(email: EmailStr, tasks: BackgroundTasks):
    tasks.add_task(fake_send_email, email, content=f"Hi [{email}], Welcome!")
    return email


@router.post("/sendemail/{email}", summary="Background task example")
def send_email(email: EmailStr, tasks: BackgroundTasks):
    tasks.add_task(fake_send_email, email, content="You are fired!")
    return {"msg": "Check the log."}


@router.post("/register", summary="Dependency injection")
def register(email: EmailStr = Depends(fake_send_register_mail)):
    return {"email": email}
