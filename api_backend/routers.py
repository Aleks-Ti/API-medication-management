from api_backend.drug_regimen.manager_routers import manager_router
from api_backend.drug_regimen.regimen_routers import regimen_router
from api_backend.user.routers import user_router

all_routers = [
    user_router,
    regimen_router,
    manager_router,
]
