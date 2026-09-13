from api_rest_contract.equipment import CreateEquipmentRequest, EquipmentResponse
from sqlalchemy.orm import Session

from api.equipment import repository as equipment_repository
from api.equipment.mappers import model_to_response, request_to_model


def list_all(session: Session) -> list[EquipmentResponse]:
    models = equipment_repository.get_all(session)
    return [model_to_response(m) for m in models]


def get_by_id(session: Session, equipment_id: str) -> EquipmentResponse | None:
    model = equipment_repository.get_by_id(session, equipment_id)
    if model is None:
        return None
    return model_to_response(model)


def create(session: Session, request: CreateEquipmentRequest) -> EquipmentResponse:
    model = request_to_model(request)
    created = equipment_repository.create(session, model)
    return model_to_response(created)


def delete(session: Session, equipment_id: str) -> bool:
    return equipment_repository.delete(session, equipment_id)
