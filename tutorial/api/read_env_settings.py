# coding=utf-8

from functools import lru_cache

from fastapi import APIRouter, Depends

from tutorial.setting import EnvFileSettings, EnvSettings


router = APIRouter()
setting = EnvSettings()
envfile_setting = EnvFileSettings()


@lru_cache
def get_setting():
    return EnvSettings()


@router.get(
    "/env_setting",
    summary="Get setting from environment variables",
    description="Pydantic will read the environment variables in a case-insensitive way",
)
def get_env_setting():
    return {
        "item1": setting.item1,
        "item2": setting.item2,
        "item3": setting.item3,
    }


@router.get("/envfile_setting", summary="Get setting from envfile")
def get_envfile_setting():
    return {
        "item4": envfile_setting.item4,
        "item5": envfile_setting.item5,
        "item6": envfile_setting.item6,
    }


@router.get("/setting_in_deps", summary="Settings in a dependency")
def setting_in_dependency(s: EnvSettings = Depends(get_setting)):
    return {
        "item1": s.item1,
        "item2": s.item2,
        "item3": s.item3,
    }
