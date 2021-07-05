# coding=utf-8

from uuid import UUID, uuid4
from datetime import datetime, date, time, timedelta, timezone
from decimal import Decimal

from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/harrypotter/", summary="Extra Python data types in query parameters")
def harry_potter(
    id: UUID = uuid4(),
    datetime_: datetime = datetime(2021, 1, 1, 23, 59, 59, 123),
    datetime_with_tz: datetime = datetime(
        2021, 1, 1, tzinfo=timezone(timedelta(hours=8))
    ),
    date_: date = date(2021, 1, 1),
    time_: time = time(23, 59, 59),
    timedelta_: timedelta = timedelta(days=1, seconds=4),
    bytes_: bytes = b"\xe4\xb8\xad\xe5\x9b\xbd",
    decimal_: Decimal = Decimal("1.00123"),
):
    return {
        "id": id,
        "datetime_": datetime_,
        "datetime_with_tz": datetime_with_tz,
        "date_": date_,
        "time_": time_,
        "timedelta_": timedelta_,
        "bytes_": bytes_,
        "decimal_": decimal_,
    }


@router.post("/up/", summary="Extra Python data types in request body")
def up(
    fronzenset_: frozenset = Body(frozenset({"iOS", "Android", "iOS"})),
):
    return {"fronzenset_": fronzenset_}
