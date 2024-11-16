from src.settings.repository import AbstractRepository
from src.tasks.repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: AbstractRepository) -> None:
        self.task_repository: TaskRepository = task_repository()
