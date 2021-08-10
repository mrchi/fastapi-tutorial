# coding=utf-8

from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    item1: str
    item2: int = 10
    item3: str = "env"


class EnvFileSettings(BaseSettings):
    item4: str
    item5: int = 20
    item6: str = "envfile"

    class Config:
        env_file = "sample.env"
        env_file_encoding = "utf-8"
