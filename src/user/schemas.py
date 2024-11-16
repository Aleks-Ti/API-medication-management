from datetime import datetime

from src.settings.schemas import PreBase


class GetUserSchema(PreBase):
    id: int
    username: str
    tg_user_id: int
    first_name: str | None
    last_name: str | None
    registered_at: datetime


class GetOrCreateUserSchema(PreBase):
    username: str
    tg_user_id: int
    first_name: str
    last_name: str


class UpdateUserSchema(PreBase):
    pass


class UserQueryParams(PreBase):
    pass
