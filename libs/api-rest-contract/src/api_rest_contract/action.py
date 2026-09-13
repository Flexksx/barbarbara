from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator, Field, Tag


class AddActionResponse(BaseModel):
    type: Literal["add"] = "add"
    material_id: str
    volume_ml: float = Field(gt=0.0)
    equipment_id: str


class PourActionResponse(BaseModel):
    type: Literal["pour"] = "pour"
    from_equipment_id: str
    to_equipment_id: str


class StrainActionResponse(BaseModel):
    type: Literal["strain"] = "strain"
    from_equipment_id: str
    to_equipment_id: str
    remove_tags: frozenset[str]


def _action_discriminator(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("type", ""))
    return str(getattr(value, "type", ""))


type ActionResponse = Annotated[
    Annotated[AddActionResponse, Tag("add")]
    | Annotated[PourActionResponse, Tag("pour")]
    | Annotated[StrainActionResponse, Tag("strain")],
    Discriminator(_action_discriminator),
]
