from src.drug_regimen.repository import ManagerRepository, RegimenRepository
from src.settings.repository import AbstractRepository


class ManagerService:
    def __init__(self, manager_repository: AbstractRepository) -> None:
        self.manager_repository: ManagerRepository = manager_repository()


class RegimenService:
    def __init__(self, regimen_repository: AbstractRepository) -> None:
        self.regimen_repository: RegimenRepository = regimen_repository()
