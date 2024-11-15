from src.event.repository import EventRepository
from src.event.service import EventService


def event_service():
    return EventService(EventRepository)
