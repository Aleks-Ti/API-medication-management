from src.event.repository import EventRepository
from src.event.schemas import CreateEventSchema, EventQueryParams, GetEventSchema, UpdateEventSchema
from src.settings.repository import AbstractRepository


class EventService:
    def __init__(self, event_repository: AbstractRepository) -> None:
        self.event_repository: EventRepository = event_repository()
