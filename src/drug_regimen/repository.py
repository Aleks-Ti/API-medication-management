from typing import Sequence

from sqlalchemy import and_, insert, select
from sqlalchemy.orm import selectinload

from src.drug_regimen.models import Manager, Regimen
from src.drug_regimen.schemas import CreateComplexManagerSchema, ManagerQueryParams, RegimenQueryParams
from src.settings.database import async_session_maker
from src.settings.repository import SQLAlchemyRepository
from src.user.models import User


class ManagerRepository(SQLAlchemyRepository):
    model: type[Manager] = Manager

    async def add_complex(self, data: CreateComplexManagerSchema) -> Manager:
        async with async_session_maker() as session:
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
                        "reception_time": data.regimen.reception_time,
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

    async def find_all_ON_user_regimen(self, query_params: ManagerQueryParams) -> Sequence[Manager]:
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .join(User, self.model.user_id == User.id)
                .options(selectinload(self.model.user), selectinload(self.model.regimens))
            )

            if query_params.user_tg_id:
                stmt = stmt.where(and_(User.tg_user_id == query_params.user_tg_id))
            if query_params.user_id:
                stmt = stmt.where(and_(User.id == query_params.user_id))
            if query_params.is_active is not None:
                stmt = stmt.where(and_(self.model.is_active == query_params.is_active))

            res = await session.execute(stmt)
            return res.scalars().all()


class RegimenRepository(SQLAlchemyRepository):
    model: type[Regimen] = Regimen

    async def find_all(self, query_params: RegimenQueryParams) -> Sequence[Regimen]:
        async with async_session_maker() as session:
            stmt = select(self.model).options(selectinload(self.model.manager).selectinload(Manager.user))

            if query_params.manager_id:
                stmt = stmt.where(and_(self.model.manager_id == query_params.manager_id))

            res = await session.execute(stmt)
            return res.scalars().all()

    async def add_one(self, data: dict) -> Regimen:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_one_ON_manager(self, id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id).options(selectinload(self.model.manager))
            res = await session.execute(stmt)
            return res.scalar_one()
