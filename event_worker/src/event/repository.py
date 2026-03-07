import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import Row
from sqlalchemy.sql import text

from src.settings.database import async_session_maker
from src.settings.repository import SQLAlchemyRepository


class EventRepository(SQLAlchemyRepository):
    async def scan_event(self) -> list[Row]:
        now_utc = datetime.now(UTC)
        interval = timedelta(minutes=1)
        start_dt = now_utc - interval
        end_dt = now_utc + interval
        async with async_session_maker() as session:
            stmt = text("""
                    SELECT
                        m.id AS manager_id,
                        m.name,
                        m.timezone,
                        r.id AS regimen_id,
                        r.reception_time,
                        r.supplement,
                        u.tg_user_id
                    FROM manager AS m
                    JOIN regimen AS r
                        ON m.id = r.manager_id
                    JOIN "user" u
                        ON u.id = m.user_id
                    WHERE
                        m.is_active = true
                        AND m.start_date <= :now
                        AND m.finish_date >= :now
                        AND r.is_active = true
                        AND (
                            CASE WHEN :start_time <= :end_time
                                THEN r.reception_time BETWEEN :start_time AND :end_time
                                ELSE r.reception_time >= :start_time OR r.reception_time <= :end_time
                            END
                        );
                """)
            params = {
                "now": now_utc,
                "start_time": start_dt.time(),
                "end_time": end_dt.time(),
            }

            res = await session.execute(stmt, params)
            return res.fetchall()
