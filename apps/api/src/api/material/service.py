from api_rest_contract.material import CreateMaterialRequest, MaterialResponse
from sqlalchemy.orm import Session

from api.material import repository as material_repository
from api.material.mappers import model_to_response, request_to_model


def list_all(session: Session) -> list[MaterialResponse]:
    models = material_repository.get_all(session)
    return [model_to_response(m) for m in models]


def get_by_id(session: Session, material_id: str) -> MaterialResponse | None:
    model = material_repository.get_by_id(session, material_id)
    if model is None:
        return None
    return model_to_response(model)


def create(session: Session, request: CreateMaterialRequest) -> MaterialResponse:
    model = request_to_model(request)
    created = material_repository.create(session, model)
    return model_to_response(created)


def delete(session: Session, material_id: str) -> bool:
    return material_repository.delete(session, material_id)
