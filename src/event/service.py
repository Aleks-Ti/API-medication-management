import asyncio
import logging
from typing import Sequence

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractRobustConnection

from src.drug_regimen.models import Manager, Regimen
from src.event.repository import EventRepository
from src.settings.configuration import config_project
from src.settings.repository import AbstractRepository
from src.user.models import User


class EventService:
    def __init__(self, event_repository: AbstractRepository, task_service: AbstractRepository = None) -> None:
        self.event_repository: EventRepository = event_repository
        self.task_service: EventRepository = task_service

    async def _send_to_rabbitmq(self, messages: list[dict]) -> None:
        connection: AbstractRobustConnection = await aio_pika.connect_robust(
            config_project.rabbit_mq.build_connection(),
        )
        try:
            async with connection as conn:
                channel: AbstractChannel = await conn.channel()
                _: AbstractQueue = await channel.declare_queue("dispatch_messages", durable=True)

                for message in messages:
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=str(message).encode(),  # Преобразуем в строку для отправки
                            content_type="application/json",
                        ),
                        routing_key="dispatch_messages",
                    )
        except Exception as err:
            print(err)

    async def scan_event(self) -> None:
        while True:
            managers: Sequence[Manager] = await self.event_repository.scan_event()
            messages = []
            if managers:
                for manager in managers:
                    user: User = manager.user
                    regimens: Regimen = manager.regimens
                    if regimens and len(regimens) == 1:
                        messages.append(
                            {
                                "tg_user_id": user.tg_user_id,
                                "manager_name": manager.name,
                                "reception_time": regimens[0].reception_time.strftime("%H:%M"),
                                "supplement": regimens[0].supplement,
                            },
                        )
                    if regimens and len(regimens) > 1:
                        for regimen in regimens:
                            messages.append(
                                {
                                    "tg_user_id": user.tg_user_id,
                                    "manager_name": manager.name,
                                    "reception_time": regimen.reception_time.strftime("%H:%M"),
                                    "supplement": regimen.supplement,
                                },
                            )
            if messages:
                logging.info(
                    "Есть сообщения для отправки!\n"
                    "спим 601 секунду, чтобы проскипать сообщения которые попали в диапазон 5 минут "
                    "(крайний случай что если сообщение впереди от now(UTC) на 299 секунд или ровно 300 "
                    "и не получиолсь так, что оно повторно попадет в очередь).",
                )
                await self._send_to_rabbitmq(messages)
                await asyncio.sleep(601.0)
            else:
                logging.info("в дейсятименутном диапазоне от now(UTC), сообщений не найдено, спим 300 секунд")
                await asyncio.sleep(300.0)
