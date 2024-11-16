from datetime import datetime, time

from src.settings.schemas import PreBase


class GetDrugRegimenSchema(PreBase):
    pass


class GetManager(PreBase):
    id: int
    name: str
    start_date: datetime
    finish_date: datetime
    timezone: str
    is_active: bool


class Regimen(PreBase):
    drug_time: time
    supplement: str
    is_active: bool


class Manager(PreBase):
    name: str
    start_date: datetime
    finish_date: datetime
    timezone: str
    is_active: bool


class CreateComplexManagerSchema(PreBase):
    user_tg_id: int
    manager: Manager
    regimen: Regimen


class AddRegimenSchema(PreBase):
    manager_id: int
    drug_time: time
    supplement: str
    is_active: bool


class UpdateDrugRegimenSchema(PreBase):
    pass


class DrugRegimenQueryParams(PreBase):
    pass
