import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.drug_regimen.dependencies import regimen_service as _regimen_service
from src.drug_regimen.schemas import (
    AddRegimenSchema,
    CreateComplexManagerSchema,
    DrugRegimenQueryParams,
    GetDrugRegimenSchema,
    UpdateDrugRegimenSchema,
)
from src.drug_regimen.service import RegimenService

regimen_router = APIRouter(
    prefix="/drug-regimen/regimen",
    tags=["regimen api"],
    responses={404: {"description": "Page not found"}},
)


@regimen_router.get("", response_model=list[GetDrugRegimenSchema])
async def get_drug_regimens(
    drug_regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    __query_params: DrugRegimenQueryParams,
) -> list[GetDrugRegimenSchema]:
    try:
        return await drug_regimen_service.drug_regimen_repository.find_all()
    except Exception as err:
        logging.exception(f"Error get a drug_regimen - {err}")
        raise HTTPException(status_code=400, detail="Error get a drug_regimen.")


@regimen_router.post("", response_model=GetDrugRegimenSchema)
async def create_drug_regimen(
    drug_regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    drug_regimen_data: CreateComplexManagerSchema,
) -> GetDrugRegimenSchema:
    try:
        return await drug_regimen_service.drug_regimen_repository.add_one(drug_regimen_data.model_dump())
    except Exception as err:
        logging.exception(f"Error create drug_regimen - {err}")
        raise HTTPException(status_code=400, detail="Error create drug_regimen.")


@regimen_router.put("/{drug_regimen_id}", response_model=GetDrugRegimenSchema)
async def update_drug_regimen(
    drug_regimen_id: int,
    drug_regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    drug_regimen_data: UpdateDrugRegimenSchema,
) -> GetDrugRegimenSchema:
    try:
        return await drug_regimen_service.drug_regimen_repository.update_one(
            drug_regimen_id,
            drug_regimen_data.model_dump(drug_regimen_id),
        )
    except Exception as err:
        logging.exception(f"Error update drug_regimen - {err}")
        raise HTTPException(status_code=400, detail="Error update drug_regimen.")


@regimen_router.get("/{drug_regimen_id}", response_model=GetDrugRegimenSchema)
async def get_drug_regimen(
    drug_regimen_id: int,
    drug_regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
) -> GetDrugRegimenSchema:
    try:
        return await drug_regimen_service.drug_regimen_repository.find_one(drug_regimen_id)
    except Exception as err:
        logging.exception(f"Error get drug_regimen by {drug_regimen_id} - {err}")
        raise HTTPException(status_code=400, detail="Error get drug_regimen by id.")


@regimen_router.delete("/{drug_regimen_id}", response_model=dict)
async def delete_drug_regimen(
    drug_regimen_id: int,
    drug_regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
) -> GetDrugRegimenSchema:
    try:
        await drug_regimen_service.drug_regimen_repository.delete_one(drug_regimen_id)
        return {"message": "Drug_Regimen deleted successfully"}
    except Exception as err:
        logging.exception(f"Error deleted drug_regimen by {drug_regimen_id} - {err}")
        raise HTTPException(status_code=400, detail="Error deleted drug_regimen by id.")


@regimen_router.post("/add", response_model=dict)
async def add_regimen(
    regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    regimen_data: AddRegimenSchema,
) -> GetDrugRegimenSchema:
    try:
        await regimen_service.regimen_repository.add_one(regimen_data.model_dump())
        return {"message": "regimen add"}
    except Exception as err:
        logging.exception(f"Error add regimen for manager_id{regimen_data.manager_id=} - {err}")
        raise HTTPException(status_code=400, detail="Error add regimen for manager.")
