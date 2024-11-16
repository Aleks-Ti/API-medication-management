from src.settings.repository import AbstractRepository
from src.user.repository import UserRepository


class UserService:
    def __init__(self, user_repository: AbstractRepository) -> None:
        self.user_repository: UserRepository = user_repository()
