from api_rest_contract.equipment import CreateEquipmentRequest, EquipmentResponse

from api.equipment.models import EquipmentModel


def request_to_model(request: CreateEquipmentRequest) -> EquipmentModel:
    return EquipmentModel(
        id=request.id,
        capacity_ml=request.capacity_ml,
        accepts_tags=list(request.accepts_tags),
    )


def model_to_response(model: EquipmentModel) -> EquipmentResponse:
    return EquipmentResponse(
        id=model.id,
        capacity_ml=model.capacity_ml,
        accepts_tags=frozenset(model.accepts_tags),
    )
