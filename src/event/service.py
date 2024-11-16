from src.event.repository import EventRepository
from src.settings.repository import AbstractRepository


class EventService:
    def __init__(self, event_repository: AbstractRepository, task_service: AbstractRepository = None) -> None:
        self.event_repository: EventRepository = event_repository
        self.task_service: EventRepository = task_service
