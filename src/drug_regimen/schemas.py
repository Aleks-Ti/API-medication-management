from datetime import datetime, time
from typing import Any

from pydantic import Field, model_validator

from src.settings.schemas import PreBase
from src.utils.time_conversion import conversion_reception_time_to_GMT


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
        data.regimen.reception_time = conversion_reception_time_to_GMT(
            data.regimen.reception_time,
            data.manager.timezone,
        )
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
