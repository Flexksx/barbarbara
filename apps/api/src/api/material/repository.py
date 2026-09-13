from sqlalchemy import select
from sqlalchemy.orm import Session

from api.material.models import MaterialModel


def get_all(session: Session) -> list[MaterialModel]:
    return list(session.execute(select(MaterialModel)).scalars().all())


def get_by_id(session: Session, material_id: str) -> MaterialModel | None:
    return session.get(MaterialModel, material_id)


def create(session: Session, model: MaterialModel) -> MaterialModel:
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def delete(session: Session, material_id: str) -> bool:
    model = session.get(MaterialModel, material_id)
    if model is None:
        return False
    session.delete(model)
    session.commit()
    return True
