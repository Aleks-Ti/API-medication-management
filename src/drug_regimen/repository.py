from sqlalchemy import insert, select

from src.drug_regimen.models import Manager, Regimen
from src.drug_regimen.schemas import CreateComplexManagerSchema
from src.settings.database import async_session_maker
from src.settings.repository import SQLAlchemyRepository
from src.user.models import User


class ManagerRepository(SQLAlchemyRepository):
    model: type[Manager] = Manager

    async def add_complex(self, data: CreateComplexManagerSchema):
        async with async_session_maker() as session:
            print(data)
            user_stmt = select(User).where(User.tg_user_id == data.user_tg_id)
            user = (await session.execute(user_stmt)).scalar_one()
            manager_stmt = (
                insert(Manager)
                .values(
                    **{
                        "name": data.manager.name,
                        "is_active": data.manager.is_active,
                        "start_date": data.manager.start_date,
                        "finish_date": data.manager.finish_date,
                        "timezone": data.manager.timezone,
                        "user_id": user.id,
                    },
                )
                .returning(Manager)
            )
            manager = await session.execute(manager_stmt)
            await session.flush()
            manager_obj = manager.scalar_one()

            regimen_stmt = (
                insert(Regimen)
                .values(
                    **{
                        "drug_time": data.regimen.drug_time,
                        "supplement": data.regimen.supplement,
                        "manager_id": manager_obj.id,
                        "is_active": data.regimen.is_active,
                    },
                )
                .returning(Regimen)
            )

            await session.execute(regimen_stmt)
            await session.commit()
            return manager_obj


class RegimenRepository(SQLAlchemyRepository):
    model: type[Regimen] = Regimen
