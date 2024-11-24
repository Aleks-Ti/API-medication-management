import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.drug_regimen.dependencies import manager_service as _manager_service
from src.drug_regimen.schemas import (
    CreateComplexManagerSchema,
    GetManagerSchema,
    GetOnlyManagerSchema,
    ManagerQueryParams,
    UpdateManagerSchema,
)
from src.drug_regimen.schemas import (
    CreateManagerSchema as CreateManagerSchema,
)
from src.drug_regimen.service import ManagerService

manager_router = APIRouter(
    prefix="/drug-regimen/manager",
    tags=["manager api"],
    responses={404: {"description": "Page not found"}},
)


@manager_router.get("", response_model=list[GetManagerSchema])
async def get_managers(
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
    query_params: Annotated[ManagerQueryParams, Query()],
):
    try:
        managers = await manager_service.manager_repository.find_all_ON_user_regimen(query_params)
        return managers
    except Exception as err:
        logging.exception(f"Error get a managers - {err}")
        raise HTTPException(status_code=400, detail="Error get a managers.")


@manager_router.post("", response_model=GetOnlyManagerSchema)
async def create_manager(
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
    manager_data: CreateManagerSchema,
):
    try:
        manager = await manager_service.manager_repository.add_one(manager_data.model_dump())
        return manager
    except Exception as err:
        logging.exception(f"Error create complex manager - {err}")
        raise HTTPException(status_code=400, detail="Error create complex manager.")


@manager_router.post("/complex", response_model=GetOnlyManagerSchema)
async def create_complex_manager(
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
    manager_data: CreateComplexManagerSchema,
):
    try:
        manager = await manager_service.manager_repository.add_complex(manager_data)
        return manager
    except Exception as err:
        logging.exception(f"Error create complex manager - {err}")
        raise HTTPException(status_code=400, detail="Error create complex manager.")


@manager_router.put("/{manager_id}", response_model=GetOnlyManagerSchema)
async def update_manager(
    manager_id: int,
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
    drug_regimen_data: UpdateManagerSchema,
):
    try:
        return await manager_service.manager_repository.update_one(
            manager_id,
            drug_regimen_data.model_dump(),
        )
    except Exception as err:
        logging.exception(f"Error update manager - {err}")
        raise HTTPException(status_code=400, detail="Error update drug_regimen.")


@manager_router.get("/{manager_id}", response_model=GetOnlyManagerSchema)
async def get_manager(
    manager_id: int,
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
):
    try:
        return await manager_service.manager_repository.find_one(manager_id)
    except Exception as err:
        logging.exception(f"Error get manager by {manager_id=} - {err}")
        raise HTTPException(status_code=400, detail="Error get manager by id.")


@manager_router.delete("/{manager_id}", response_model=dict)
async def delete_manager(
    manager_id: int,
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
):
    try:
        await manager_service.manager_repository.delete_one(manager_id)
        return {"message": "manager deleted successfully"}
    except Exception as err:
        logging.exception(f"Error deleted manager by {manager_id=} - {err}")
        raise HTTPException(status_code=400, detail="Error deleted manager by id.")
