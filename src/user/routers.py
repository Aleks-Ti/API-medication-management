import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.user.dependencies import user_service as _user_service
from src.user.schemas import GetOrCreateUserSchema, GetUserSchema, UpdateUserSchema, UserQueryParams
from src.user.service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user api"],
    responses={404: {"description": "Page not found"}},
)


@user_router.get("", response_model=list[GetUserSchema])
async def get_users(
    user_service: Annotated[UserService, Depends(_user_service)],
    query_params: Annotated[UserQueryParams, Depends(UserQueryParams)],
) -> list[GetUserSchema]:
    try:
        return await user_service.user_repository.find_all()
    except Exception as err:
        logging.exception(f"Error get a user - {err}")
        raise HTTPException(status_code=400, detail="Error get a user.")


@user_router.post("", response_model=GetUserSchema)
async def get_or_create_user(
    user_service: Annotated[UserService, Depends(_user_service)],
    user_data: GetOrCreateUserSchema,
) -> GetUserSchema:
    try:
        user = await user_service.user_repository.get_or_create_user(user_data)
        return user
    except Exception as err:
        logging.exception(f"Error create user - {err}")
        raise HTTPException(status_code=400, detail="Error create user.")


@user_router.patch("/{user_id}", response_model=GetUserSchema)
async def update_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(_user_service)],
    user_data: UpdateUserSchema,
) -> GetUserSchema:
    try:
        return await user_service.user_repository.update_one(user_id, user_data.model_dump(user_id))
    except Exception as err:
        logging.exception(f"Error update user - {err}")
        raise HTTPException(status_code=400, detail="Error update user.")


@user_router.get("/{user_id}", response_model=GetUserSchema)
async def get_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(_user_service)],
) -> GetUserSchema:
    try:
        return await user_service.user_repository.find_one(user_id)
    except Exception as err:
        logging.exception(f"Error get user by {user_id} - {err}")
        raise HTTPException(status_code=400, detail="Error get user by id.")


@user_router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(_user_service)],
) -> GetUserSchema:
    try:
        await user_service.user_repository.delete_one(user_id)
        return {"message": "User deleted successfully"}
    except Exception as err:
        logging.exception(f"Error deleted user by {user_id} - {err}")
        raise HTTPException(status_code=400, detail="Error deleted user by id.")
