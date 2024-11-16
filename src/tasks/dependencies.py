from src.tasks.repository import TaskRepository
from src.tasks.service import TaskService


def task_service():
    return TaskService(TaskRepository)
