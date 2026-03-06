from tg_bot.user.requests import UserApiClient
from tg_bot.user.service import UserService


def user_service():
    return UserService(UserApiClient())
