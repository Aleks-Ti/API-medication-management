import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.drug_regimen.dependencies import manager_service as _manager_service
from src.drug_regimen.schemas import (
    CreateComplexManagerSchema,
    DrugRegimenQueryParams,
    GetDrugRegimenSchema,
    GetManager,
    UpdateDrugRegimenSchema,
)
from src.drug_regimen.service import ManagerService

manager_router = APIRouter(
    prefix="/drug-regimen/manager",
    tags=["manager api"],
    responses={404: {"description": "Page not found"}},
)


@manager_router.get("", response_model=list[GetDrugRegimenSchema])
async def get_drug_regimens(
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
    __query_params: DrugRegimenQueryParams,
) -> list[GetDrugRegimenSchema]:
    try:
        return await manager_service.drug_regimen_repository.find_all()
    except Exception as err:
        logging.exception(f"Error get a drug_regimen - {err}")
        raise HTTPException(status_code=400, detail="Error get a drug_regimen.")


@manager_router.post("/complex", response_model=GetManager)
async def create_drug_regimen(
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
    manager_data: CreateComplexManagerSchema,
) -> GetDrugRegimenSchema:
    try:
        return await manager_service.manager_repository.add_complex(manager_data)
    except Exception as err:
        logging.exception(f"Error create drug_regimen - {err}")
        raise HTTPException(status_code=400, detail="Error create drug_regimen.")


@manager_router.put("/{drug_regimen_id}", response_model=GetDrugRegimenSchema)
async def update_drug_regimen(
    drug_regimen_id: int,
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
    drug_regimen_data: UpdateDrugRegimenSchema,
) -> GetDrugRegimenSchema:
    try:
        return await manager_service.drug_regimen_repository.update_one(
            drug_regimen_id,
            drug_regimen_data.model_dump(drug_regimen_id),
        )
    except Exception as err:
        logging.exception(f"Error update drug_regimen - {err}")
        raise HTTPException(status_code=400, detail="Error update drug_regimen.")


@manager_router.get("/{drug_regimen_id}", response_model=GetDrugRegimenSchema)
async def get_drug_regimen(
    drug_regimen_id: int,
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
) -> GetDrugRegimenSchema:
    try:
        return await manager_service.drug_regimen_repository.find_one(drug_regimen_id)
    except Exception as err:
        logging.exception(f"Error get drug_regimen by {drug_regimen_id} - {err}")
        raise HTTPException(status_code=400, detail="Error get drug_regimen by id.")


@manager_router.delete("/{drug_regimen_id}", response_model=dict)
async def delete_drug_regimen(
    drug_regimen_id: int,
    manager_service: Annotated[ManagerService, Depends(_manager_service)],
) -> GetDrugRegimenSchema:
    try:
        await manager_service.drug_regimen_repository.delete_one(drug_regimen_id)
        return {"message": "Drug_Regimen deleted successfully"}
    except Exception as err:
        logging.exception(f"Error deleted drug_regimen by {drug_regimen_id} - {err}")
        raise HTTPException(status_code=400, detail="Error deleted drug_regimen by id.")
