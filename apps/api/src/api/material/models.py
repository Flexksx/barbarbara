from typing import Any

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from api.database import Base


class MaterialModel(Base):
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column(primary_key=True)
    ph: Mapped[float]
    brix: Mapped[float]
    abv: Mapped[float]
    density: Mapped[float]
    tags: Mapped[list[Any]] = mapped_column(JSON, default=list)
    constraints: Mapped[list[Any]] = mapped_column(JSON, default=list)
