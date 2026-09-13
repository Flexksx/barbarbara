from pydantic import BaseModel

from api_rest_contract.constraint import ConstraintResponse
from api_rest_contract.properties import PropertiesResponse


class CreateMaterialRequest(BaseModel):
    id: str
    properties: PropertiesResponse
    tags: frozenset[str]
    constraints: tuple[ConstraintResponse, ...] = ()


class MaterialResponse(BaseModel):
    id: str
    properties: PropertiesResponse
    tags: frozenset[str]
    constraints: tuple[ConstraintResponse, ...] = ()
