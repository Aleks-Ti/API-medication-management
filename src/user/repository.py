from sqlalchemy import insert, select

from src.settings.database import async_session_maker
from src.settings.repository import SQLAlchemyRepository
from src.user.models import User
from src.user.schemas import GetOrCreateUserSchema


class UserRepository(SQLAlchemyRepository):
    model: type[User] = User

    async def get_or_create_user(self, user_data: GetOrCreateUserSchema) -> User:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.tg_user_id == user_data.tg_user_id)
            result = (await session.execute(stmt)).scalar_one_or_none()
            if result is None:
                dict_user_data = {
                    "username": user_data.username,
                    "tg_user_id": user_data.tg_user_id,
                    "first_name": user_data.first_name,
                    "last_name": user_data.last_name,
                }

                stmt_user = insert(self.model).values(**dict_user_data).returning(self.model)
                result_user = await session.execute(stmt_user)
                await session.commit()
                result = result_user.scalar_one()

            return result

    async def find_all(self) -> list[User]:
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().all()
