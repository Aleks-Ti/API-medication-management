import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.event.dependencies import event_service as _event_service
from src.event.schemas import CreateEventSchema, EventQueryParams, GetEventSchema, UpdateEventSchema
from src.event.service import EventService

event_router = APIRouter(
    prefix="/event",
    tags=["event api"],
    responses={404: {"description": "Page not found"}},
)


@event_router.get("", response_model=list[GetEventSchema])
async def get_events(
    event_service: Annotated[EventService, Depends(_event_service)],
    __query_params: EventQueryParams,
) -> list[GetEventSchema]:
    try:
        return await event_service.event_repository.find_all()
    except Exception as err:
        logging.exception(f"Error get a event - {err}")
        raise HTTPException(status_code=400, detail="Error get a event.")


@event_router.post("", response_model=GetEventSchema)
async def create_event(
    event_service: Annotated[EventService, Depends(_event_service)],
    event_data: CreateEventSchema,
) -> GetEventSchema:
    try:
        return await event_service.event_repository.add_one(event_data.model_dump())
    except Exception as err:
        logging.exception(f"Error create event - {err}")
        raise HTTPException(status_code=400, detail="Error create event.")


@event_router.put("/event_id", response_model=GetEventSchema)
async def update_event(
    event_id: int,
    event_service: Annotated[EventService, Depends(_event_service)],
    event_data: UpdateEventSchema,
) -> GetEventSchema:
    try:
        return await event_service.event_repository.update_one(event_id, event_data.model_dump(event_id))
    except Exception as err:
        logging.exception(f"Error update event - {err}")
        raise HTTPException(status_code=400, detail="Error update event.")


@event_router.get("/event_id", response_model=GetEventSchema)
async def get_event(
    event_id: int,
    event_service: Annotated[EventService, Depends(_event_service)],
) -> GetEventSchema:
    try:
        return await event_service.event_repository.find_one(event_id)
    except Exception as err:
        logging.exception(f"Error get event by {event_id} - {err}")
        raise HTTPException(status_code=400, detail="Error get event by id.")


@event_router.delete("/event_id", response_model=dict)
async def delete_event(
    event_id: int,
    event_service: Annotated[EventService, Depends(_event_service)],
) -> GetEventSchema:
    try:
        await event_service.event_repository.delete_one(event_id)
        return {"message": "Event deleted successfully"}
    except Exception as err:
        logging.exception(f"Error deleted event by {event_id} - {err}")
        raise HTTPException(status_code=400, detail="Error deleted event by id.")
