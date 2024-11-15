import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.settings.base_model import Base


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)
