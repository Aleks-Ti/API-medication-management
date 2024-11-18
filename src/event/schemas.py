from datetime import time

from src.settings.schemas import PreBase


class EventMessageSchema(PreBase):
    tg_user_id: int
    manager_name: str
    reception_time: time
    supplement: str


class CreateEventSchema(PreBase):
    pass


class UpdateEventSchema(PreBase):
    pass


class EventQueryParams(PreBase):
    pass
