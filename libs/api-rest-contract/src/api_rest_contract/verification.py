from pydantic import BaseModel

from api_rest_contract.action import ActionResponse
from api_rest_contract.equipment import EquipmentResponse
from api_rest_contract.material import MaterialResponse


class StepViolationResponse(BaseModel):
    step: int
    kind: str
    message: str


class VerifyPlanRequest(BaseModel):
    actions: list[ActionResponse]
    materials: dict[str, MaterialResponse]
    equipment: dict[str, EquipmentResponse]


class VerifyPlanResponse(BaseModel):
    valid: bool
    violations: list[StepViolationResponse]
    equipment_states: dict[str, EquipmentResponse]
