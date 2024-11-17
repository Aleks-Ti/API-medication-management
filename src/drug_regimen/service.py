from datetime import datetime, time, timedelta

from src.drug_regimen.repository import ManagerRepository, RegimenRepository
from src.drug_regimen.schemas import DICT_TIMEZONE, MSK_TIME_ZONE, AddRegimenSchema
from src.settings.repository import AbstractRepository


class ManagerService:
    def __init__(self, manager_repository: AbstractRepository) -> None:
        self.manager_repository: ManagerRepository = manager_repository


class RegimenService:
    def __init__(self, regimen_repository: AbstractRepository, manager_repository: AbstractRepository) -> None:
        self.regimen_repository: RegimenRepository = regimen_repository
        self.manager_repository: ManagerRepository = manager_repository

    @staticmethod
    async def get_reception_time_GMT(reception_time: time, timezone: str) -> dict:
        time_from_data = datetime.combine(datetime(2024, 1, 1), reception_time)
        # _time = time_from_data - timedelta(hours=3)
        result = (time_from_data - timedelta(hours=DICT_TIMEZONE[timezone](MSK_TIME_ZONE))).time()
        return result

    async def add_one_complex(self, regimen_data: AddRegimenSchema):
        manager_obj = await self.manager_repository.find_one(regimen_data.manager_id)

        dict_regimen_data = regimen_data.model_dump()
        dict_regimen_data["reception_time"] = await self.get_reception_time_GMT(
            regimen_data.reception_time,
            manager_obj.timezone,
        )

        regimen = await self.regimen_repository.add_one(dict_regimen_data)
        return regimen
