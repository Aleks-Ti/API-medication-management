from src.drug_regimen.repository import ManagerRepository, RegimenRepository
from src.drug_regimen.schemas import AddRegimenSchema
from src.settings.repository import AbstractRepository
from src.utils.time_conversion import conversion_reception_time_to_GMT


class ManagerService:
    def __init__(self, manager_repository: AbstractRepository) -> None:
        self.manager_repository: ManagerRepository = manager_repository


class RegimenService:
    def __init__(self, regimen_repository: AbstractRepository, manager_repository: AbstractRepository) -> None:
        self.regimen_repository: RegimenRepository = regimen_repository
        self.manager_repository: ManagerRepository = manager_repository
        self.conversion_time = conversion_reception_time_to_GMT

    async def add_one_complex(self, regimen_data: AddRegimenSchema):
        manager_obj = await self.manager_repository.find_one(regimen_data.manager_id)

        dict_regimen_data = regimen_data.model_dump()
        dict_regimen_data["reception_time"] = self.conversion_time(
            regimen_data.reception_time,
            manager_obj.timezone,
        )

        regimen = await self.regimen_repository.add_one(dict_regimen_data)
        return regimen
