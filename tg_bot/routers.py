from aiogram.dispatcher.router import Router

from tg_bot.drug_regimen.handlers import drug_regimen_router
from tg_bot.drug_regimen_manager.handlers import drug_regimen_manager_router
from tg_bot.service_handlers import start_router

all_routers: list[Router] = [
    start_router,
    drug_regimen_router,
    drug_regimen_manager_router,
]
