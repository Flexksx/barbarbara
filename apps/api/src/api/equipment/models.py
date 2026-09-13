from typing import Any

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from api.database import Base


class EquipmentModel(Base):
    __tablename__ = "equipment"

    id: Mapped[str] = mapped_column(primary_key=True)
    capacity_ml: Mapped[float]
    accepts_tags: Mapped[list[Any]] = mapped_column(JSON, default=list)
