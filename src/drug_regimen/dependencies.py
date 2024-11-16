from src.drug_regimen.repository import ManagerRepository, RegimenRepository
from src.drug_regimen.service import ManagerService, RegimenService


def manager_service():
    return ManagerService(ManagerRepository)


def regimen_service():
    return RegimenService(RegimenRepository)
