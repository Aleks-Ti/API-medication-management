from src.settings.database import async_session_maker
from src.settings.repository import SQLAlchemyRepository
from src.event.models import Event


class EventRepository(SQLAlchemyRepository):
    model: type[Event] = Event
