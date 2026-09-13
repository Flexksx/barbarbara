from pydantic import BaseModel, Field

from api_rest_contract.mixture import MixtureResponse


class CreateEquipmentRequest(BaseModel):
    id: str
    capacity_ml: float = Field(gt=0.0)
    accepts_tags: frozenset[str]


class EquipmentResponse(BaseModel):
    id: str
    capacity_ml: float = Field(gt=0.0)
    accepts_tags: frozenset[str]
    contents: MixtureResponse | None = None
