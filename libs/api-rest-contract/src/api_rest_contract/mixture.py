from pydantic import BaseModel, Field

from api_rest_contract.properties import PropertiesResponse


class MixtureComponentResponse(BaseModel):
    material_id: str
    volume_ml: float = Field(gt=0.0)


class MixtureResponse(BaseModel):
    components: tuple[MixtureComponentResponse, ...] = ()
    total_volume_ml: float = Field(ge=0.0)
    properties: PropertiesResponse | None = None
