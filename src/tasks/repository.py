from src.settings.database import async_session_maker  # noqa: F401
from src.settings.repository import SQLAlchemyRepository
from src.tasks.models import Task


class TaskRepository(SQLAlchemyRepository):
    model: type[Task] = Task
