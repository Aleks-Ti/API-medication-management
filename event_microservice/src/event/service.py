import asyncio
import logging
from datetime import time

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractRobustConnection
from sqlalchemy import Row

from src.event.repository import EventRepository
from src.settings.configuration import config_project
from src.settings.repository import AbstractRepository
from src.utils.time_conversion import conversion_GMT_reception_time_to_TZ


class EventService:
    def __init__(self, event_repository: AbstractRepository) -> None:
        self.event_repository: EventRepository = event_repository
        self.conversion_time = conversion_GMT_reception_time_to_TZ

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
            logging.error(f"Произошла ошибка при отправке сообщения в очередь: {err}")
            raise

    async def scan_event(self) -> None:
        while True:
            managers: list[Row] = await self.event_repository.scan_event()
            messages = []
            if managers:
                for manager in managers:
                    reception_time: time = self.conversion_time(manager.reception_time, manager.timezone)
                    messages.append(
                        {
                            "tg_user_id": manager.tg_user_id,
                            "manager_id": manager.manager_id,
                            "manager_name": manager.name,
                            "regimen_id": manager.regimen_id,
                            "reception_time": reception_time.strftime("%H:%M"),
                            "supplement": manager.supplement,
                        },
                    )

            if messages:
                logging.info(
                    "Есть сообщения для отправки!\n"
                    "спим 61 секунду, чтобы проскипать сообщения которые попали в диапазон 5 минут "
                    "(крайний случай что если сообщение впереди от now(UTC) на 299 секунд или ровно 300 "
                    "и не получиолсь так, что оно повторно попадет в очередь).",
                )
                await self._send_to_rabbitmq(messages)
                await asyncio.sleep(121.0)
            else:
                logging.info("в двух минутном диапазоне от now(UTC), сообщений не найдено, спим 30 секунд")
                await asyncio.sleep(30.0)
