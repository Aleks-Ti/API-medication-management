from datetime import datetime, time, timedelta
from typing import Any

from pydantic import Field, model_validator

from src.settings.schemas import PreBase

MSK_TIME_ZONE = 3  # часовой пояс МСК от гринвича

DICT_TIMEZONE = {
    "-1": lambda x: x - 1,
    "МСК": lambda x: x,
    "+1": lambda x: x + 1,
    "+2": lambda x: x + 2,
    "+3": lambda x: x + 3,
    "+4": lambda x: x + 4,
    "+5": lambda x: x + 5,
    "+6": lambda x: x + 6,
    "+7": lambda x: x + 7,
    "+8": lambda x: x + 8,
    "+9": lambda x: x + 9,
}


class GetOnlyManagerSchema(PreBase):
    id: int
    name: str
    start_date: datetime
    finish_date: datetime
    timezone: str
    is_active: bool


class CreateComplexRegimenSchema(PreBase):
    reception_time: time
    supplement: str
    is_active: bool


class CreateComplexManagerSchema(PreBase):
    name: str
    start_date: datetime
    finish_date: datetime
    timezone: str
    is_active: bool


class CreateComplexManagerSchema(PreBase):
    user_tg_id: int
    manager: CreateComplexManagerSchema
    regimen: CreateComplexRegimenSchema

    @model_validator(mode="after")
    @classmethod
    def set_reception_time_GMT(cls, data) -> Any:
        msk_time_zone = MSK_TIME_ZONE
        time_from_data = datetime.combine(datetime(2024, 1, 1), data.regimen.reception_time)
        data.regimen.reception_time = (
            time_from_data - timedelta(hours=DICT_TIMEZONE[data.manager.timezone](msk_time_zone))
        ).time()
        return data


class AddRegimenSchema(PreBase):
    manager_id: int
    reception_time: time
    supplement: str
    is_active: bool


class CreateManagerSchema(PreBase):
    user_id: int
    name: str
    start_date: datetime
    finish_date: datetime
    timezone: str
    is_active: bool


class UpdateManagerSchema(PreBase):
    user_id: int = Field(None)
    name: str = Field(None)
    start_date: datetime = Field(None)
    finish_date: datetime = Field(None)
    timezone: str = Field(None)
    is_active: bool = Field(None)


class GetRegimenSchema(PreBase):
    id: int
    reception_time: time
    supplement: str
    is_active: bool


class GetUserSchema(PreBase):
    id: int
    username: str
    tg_user_id: int
    first_name: str | None
    last_name: str | None
    registered_at: datetime


class GetManagerSchema(PreBase):
    id: int
    name: str
    start_date: datetime
    finish_date: datetime
    timezone: str
    is_active: bool
    regimens: list[GetRegimenSchema]
    user: GetUserSchema


class ManagerQueryParams(PreBase):
    user_tg_id: int = Field(None)
    user_id: int = Field(None)
    is_active: bool = Field(None)


class RegimenQueryParams(PreBase):
    manager_id: int = Field(None)


class GetRegimenSchema(PreBase):
    id: int
    reception_time: time
    supplement: str
    is_active: bool
    manager: GetOnlyManagerSchema
    user: GetUserSchema

    @model_validator(mode="before")
    @classmethod
    def set_manager(cls, data) -> Any:
        data.user = data.manager.user
        return data


class CreateRegimenSchema(PreBase):
    manager_id: int
    reception_time: time
    supplement: str
    is_active: bool


class GetOnlyRegimenSchema(PreBase):
    id: int
    reception_time: time
    supplement: str
    is_active: bool
    manager_id: int


class UpdateRegimenSchema(PreBase):
    reception_time: time = Field(None)
    supplement: str = Field(None)
    is_active: bool = Field(None)
