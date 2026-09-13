from sqlalchemy import select
from sqlalchemy.orm import Session

from api.equipment.models import EquipmentModel


def get_all(session: Session) -> list[EquipmentModel]:
    return list(session.execute(select(EquipmentModel)).scalars().all())


def get_by_id(session: Session, equipment_id: str) -> EquipmentModel | None:
    return session.get(EquipmentModel, equipment_id)


def create(session: Session, model: EquipmentModel) -> EquipmentModel:
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def delete(session: Session, equipment_id: str) -> bool:
    model = session.get(EquipmentModel, equipment_id)
    if model is None:
        return False
    session.delete(model)
    session.commit()
    return True
