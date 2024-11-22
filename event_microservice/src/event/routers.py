import logging

from fastapi import APIRouter, HTTPException

from src.event.schemas import CheckLiveServiceSchema

event_router = APIRouter(
    prefix="/event",
    tags=["event api"],
    responses={404: {"description": "Page not found"}},
)


@event_router.get("", response_model=dict)
async def alive_events() -> CheckLiveServiceSchema:
    try:
        return {"message": "event server alive"}
    except Exception as err:
        logging.exception(f"Error get alive_events - {err}")
        raise HTTPException(status_code=400, detail="Error get a alive_events.")
