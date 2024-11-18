from datetime import UTC, datetime, timedelta

from sqlalchemy import Row, Time, cast, select

from src.drug_regimen.models import Manager, Regimen
from src.settings.database import async_session_maker
from src.settings.repository import SQLAlchemyRepository
from src.user.models import User


class EventRepository(SQLAlchemyRepository):
    async def scan_event(self) -> list[Row]:
        now_utc = datetime.now(UTC)
        interval = timedelta(minutes=1)
        start_time = (now_utc - interval).time()
        end_time = (now_utc + interval).time()
        async with async_session_maker() as session:
            stmt = (
                select(Manager.name, Manager.timezone, Regimen.reception_time, Regimen.supplement, User.tg_user_id)
                .join(Regimen, Manager.id == Regimen.manager_id, isouter=True)
                .join(User, Manager.user_id == User.id)
                .where(
                    Manager.is_active == True,  # noqa: E712
                    Manager.start_date <= now_utc,
                    Manager.finish_date >= now_utc,
                    Regimen.is_active == True,  # noqa: E712
                    Regimen.reception_time.between(
                        cast(start_time, Time),
                        cast(end_time, Time),
                    ),
                )
            )
            res = await session.execute(stmt)
            return res.fetchall()
