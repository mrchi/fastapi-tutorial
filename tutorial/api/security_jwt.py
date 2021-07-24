# coding=utf-8

import arrow
from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

JWT_SECRET_KEY = "632b148d76e85e2a13832a1ed466916211b5feea496c5353155674788f0671cf"
JWT_EXPIRE_MINUTES = 3
JWT_ALGORITHM = "HS256"

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/securityjwt/token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "fullname": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    user = UserInDB(**user)
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expire_delta: int = JWT_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = arrow.now().shift(minutes=expire_delta).timestamp()
    to_encode |= {"expire": int(expire)}
    access_token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return access_token


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credential_exception
    current_user = UserInDB(**user)
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


@router.post("/token", response_model=Token, summary="Login for access token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User, summary="Protected by JWT access token")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
