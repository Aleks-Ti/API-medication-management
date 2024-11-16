from src.drug_regimen.manager_routers import manager_router
from src.drug_regimen.regimen_routers import regimen_router
from src.user.routers import user_router

all_routers = [
    user_router,
    regimen_router,
    manager_router,
]
