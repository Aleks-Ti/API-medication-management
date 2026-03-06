from api_backend.user.repository import UserRepository
from api_backend.user.service import UserService


def user_service():
    return UserService(UserRepository())
