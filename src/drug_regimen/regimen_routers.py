import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.drug_regimen.dependencies import regimen_service as _regimen_service
from src.drug_regimen.schemas import (
    AddRegimenSchema,
    CreateRegimenSchema,
    GetOnlyRegimenSchema,
    GetRegimenSchema,
    RegimenQueryParams,
    UpdateRegimenSchema,
)
from src.drug_regimen.service import RegimenService

regimen_router = APIRouter(
    prefix="/drug-regimen/regimen",
    tags=["regimen api"],
    responses={404: {"description": "Page not found"}},
)


@regimen_router.get("", response_model=list[GetRegimenSchema])
async def get_regimens(
    regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    query_params: Annotated[RegimenQueryParams, Query()],
) -> list[GetRegimenSchema]:
    try:
        regimens = await regimen_service.regimen_repository.find_all(query_params)
        return regimens
    except Exception as err:
        logging.exception(f"Error get a drug_regimen - {err}")
        raise HTTPException(status_code=400, detail="Error get a drug_regimen.")


@regimen_router.post("", response_model=GetOnlyRegimenSchema)
async def create_regimen(
    regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    regimen_data: CreateRegimenSchema,
) -> GetRegimenSchema:
    try:
        return await regimen_service.regimen_repository.add_one(regimen_data.model_dump())
    except Exception as err:
        logging.exception(f"Error create regimen - {err}")
        raise HTTPException(status_code=400, detail="Error create regimen.")


@regimen_router.put("/{regimen_id}", response_model=GetOnlyRegimenSchema)
async def update_regimen(
    regimen_id: int,
    regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    regimen_data: UpdateRegimenSchema,
) -> GetRegimenSchema:
    try:
        return await regimen_service.regimen_repository.update_one(
            regimen_id,
            regimen_data.model_dump(),
        )
    except Exception as err:
        logging.exception(f"Error update regimen - {err}")
        raise HTTPException(status_code=400, detail="Error update regimen.")


@regimen_router.get("/{regimen_id}", response_model=GetOnlyRegimenSchema)
async def get_regimen(
    regimen_id: int,
    regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
) -> GetRegimenSchema:
    try:
        return await regimen_service.regimen_repository.find_one(regimen_id)
    except Exception as err:
        logging.exception(f"Error get regimen by {regimen_id} - {err}")
        raise HTTPException(status_code=400, detail="Error get regimen by id.")


@regimen_router.delete("/{regimen_id}", response_model=dict)
async def delete_regimen(
    regimen_id: int,
    regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
) -> dict:
    try:
        await regimen_service.regimen_repository.delete_one(regimen_id)
        return {"message": "regimen deleted successfully"}
    except Exception as err:
        logging.exception(f"Error deleted regimen by {regimen_id} - {err}")
        raise HTTPException(status_code=400, detail="Error deleted regimen by id.")


@regimen_router.post("/complex", response_model=dict)
async def add_regimen(
    regimen_service: Annotated[RegimenService, Depends(_regimen_service)],
    regimen_data: AddRegimenSchema,
) -> dict:
    try:
        await regimen_service.regimen_repository.add_one(regimen_data.model_dump())
        return {"message": "regimen add successfully"}
    except Exception as err:
        logging.exception(f"Error add regimen for manager_id{regimen_data.manager_id=} - {err}")
        raise HTTPException(status_code=400, detail="Error add regimen for manager.")
