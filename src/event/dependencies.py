from src.event.repository import EventRepository
from src.event.service import EventService
from src.settings.fabric_dependency import DependsFactory
from src.tasks.dependencies import task_service


class EventFactory(DependsFactory):
    def __init__(self, modes) -> None:
        super().__init__(modes, "task")

    def get_service(self) -> EventService:
        if self.modes:
            for mode in self.modes:
                if mode == "task":
                    self.authorised_mode["task"] = task_service()

        event_service = EventService(
            event_repository=EventRepository(),
            task_service=self.authorised_mode["task"],
        )

        return event_service


def event_service(*modes: str) -> EventService:
    factory = EventFactory(modes)
    return factory.get_service()
