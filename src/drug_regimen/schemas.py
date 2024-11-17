from datetime import datetime, time

from pydantic import Field

from src.settings.schemas import PreBase


class GetDrugRegimenSchema(PreBase):
    pass


class GetOnlyManagerSchema(PreBase):
    id: int
    name: str
    start_date: datetime
    finish_date: datetime
    timezone: str
    is_active: bool


class CreateComplexRegimenSchema(PreBase):
    drug_time: time
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


class AddRegimenSchema(PreBase):
    manager_id: int
    drug_time: time
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
    drug_time: time
    supplement: str
    is_active: bool


class GetUserSchema(PreBase):
    id: int
    username: str
    tg_user_id: int
    first_name: str
    last_name: str
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
