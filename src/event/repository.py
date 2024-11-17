from datetime import UTC, datetime, timedelta
from typing import Sequence

from sqlalchemy import Time, cast, select
from sqlalchemy.orm import selectinload

from src.drug_regimen.models import Manager, Regimen
from src.settings.database import async_session_maker
from src.settings.repository import SQLAlchemyRepository


class EventRepository(SQLAlchemyRepository):
    async def scan_event(self) -> Sequence[Manager]:
        now_utc = datetime.now(UTC)
        interval = timedelta(minutes=5)
        start_time = (now_utc - interval).time()
        end_time = (now_utc + interval).time()
        async with async_session_maker() as session:
            stmt = (
                select(Manager)
                .join(Regimen, Manager.id == Regimen.manager_id)
                .options(selectinload(Manager.regimens), selectinload(Manager.user))
            )
            stmt = stmt.where(
                Manager.is_active == True,  # noqa: E712
                Manager.start_date <= now_utc,
                Manager.finish_date >= now_utc,
                Regimen.is_active == True,  # noqa: E712
                Regimen.reception_time.between(
                    cast(start_time, Time),
                    cast(end_time, Time),
                ),
            )
            res = await session.execute(stmt)

            return res.scalars().all()
