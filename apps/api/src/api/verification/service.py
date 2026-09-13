from api_core.verification import verify
from api_rest_contract.verification import VerifyPlanRequest, VerifyPlanResponse

from api.verification.mappers import (
    action_to_core,
    equipment_to_core,
    material_to_core,
    result_to_response,
)


def verify_plan(request: VerifyPlanRequest) -> VerifyPlanResponse:
    materials = {k: material_to_core(v) for k, v in request.materials.items()}
    equipment = {k: equipment_to_core(v) for k, v in request.equipment.items()}
    actions = [action_to_core(a) for a in request.actions]

    result = verify(actions, materials, equipment)

    return result_to_response(result)
