import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.tasks.dependencies import task_service as _task_service
from src.tasks.schemas import CreateTaskSchema, GetTaskSchema, TaskQueryParams, UpdateTaskSchema
from src.tasks.service import TaskService

task_router = APIRouter(
    prefix="/task",
    tags=["task api"],
    responses={404: {"description": "Page not found"}},
)


@task_router.get("", response_model=list[GetTaskSchema])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(_task_service)],
    __query_params: TaskQueryParams,
) -> list[GetTaskSchema]:
    try:
        return await task_service.task_repository.find_all()
    except Exception as err:
        logging.exception(f"Error get a task - {err}")
        raise HTTPException(status_code=400, detail="Error get a task.")


@task_router.post("", response_model=GetTaskSchema)
async def create_task(
    task_service: Annotated[TaskService, Depends(_task_service)],
    task_data: CreateTaskSchema,
) -> GetTaskSchema:
    try:
        return await task_service.task_repository.add_one(task_data.model_dump())
    except Exception as err:
        logging.exception(f"Error create task - {err}")
        raise HTTPException(status_code=400, detail="Error create task.")


@task_router.put("/{task_id}", response_model=GetTaskSchema)
async def update_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(_task_service)],
    task_data: UpdateTaskSchema,
) -> GetTaskSchema:
    try:
        return await task_service.task_repository.update_one(task_id, task_data.model_dump(task_id))
    except Exception as err:
        logging.exception(f"Error update task - {err}")
        raise HTTPException(status_code=400, detail="Error update task.")


@task_router.get("/{task_id}", response_model=GetTaskSchema)
async def get_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(_task_service)],
) -> GetTaskSchema:
    try:
        return await task_service.task_repository.find_one(task_id)
    except Exception as err:
        logging.exception(f"Error get task by {task_id} - {err}")
        raise HTTPException(status_code=400, detail="Error get task by id.")


@task_router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(_task_service)],
) -> GetTaskSchema:
    try:
        await task_service.task_repository.delete_one(task_id)
        return {"message": "Task deleted successfully"}
    except Exception as err:
        logging.exception(f"Error deleted task by {task_id} - {err}")
        raise HTTPException(status_code=400, detail="Error deleted task by id.")
