from pydantic import BaseModel, Field


class PropertiesResponse(BaseModel):
    ph: float = Field(ge=0.0, le=14.0)
    brix: float = Field(ge=0.0)
    abv: float = Field(ge=0.0, le=1.0)
    density: float = Field(gt=0.0)
