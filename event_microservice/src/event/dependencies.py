from src.event.repository import EventRepository
from src.event.service import EventService


def event_service() -> EventService:
    return EventService(EventRepository())
