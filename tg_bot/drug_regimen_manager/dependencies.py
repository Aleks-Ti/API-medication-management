from tg_bot.drug_regimen.requests import ManagerApiClient, RegimenApiClient
from tg_bot.drug_regimen_manager.service import DrManagerService
from tg_bot.user.dependencies import user_service
from tg_bot.user.requests import UserApiClient


def dr_manager_service() -> DrManagerService:
    return DrManagerService(ManagerApiClient(), RegimenApiClient(), UserApiClient())
