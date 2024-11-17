import asyncio
from typing import Sequence

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
        """
        Отправляет сообщения в RabbitMQ.
        """
        import aio_pika

        connection: AbstractRobustConnection = await aio_pika.connect_robust(
            config_project.rabbit_mq.build_connection(),
        )
        try:
            async with connection as conn:
                channel: AbstractChannel = await conn.channel()
                _: AbstractQueue = await channel.declare_queue("send_tg_message", durable=True)

                for message in messages:
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=str(message).encode(),  # Преобразуем в строку для отправки
                            content_type="application/json",
                        ),
                        routing_key="send_tg_message",
                    )
        except Exception as err:
            print(err)

    async def scan_event(self) -> None:
        count = 0
        while True:
            count += 1
            print("new circle", count)
            managers: Sequence[Manager] = await self.event_repository.scan_event()
            messages = []
            if managers:
                for manager in managers:
                    user: User = manager.user
                    regimen: Regimen = manager.regimens
                    if regimen:
                        messages.append(
                            {
                                "tg_user_id": user.tg_user_id,
                                "manager_name": manager.name,
                                "reception_time": regimen[0].reception_time,
                                "supplement": regimen[0].supplement,
                            },
                        )
            if messages:
                print("есть че")
                await self._send_to_rabbitmq(messages)
            print("я спать")
            await asyncio.sleep(360.0)
