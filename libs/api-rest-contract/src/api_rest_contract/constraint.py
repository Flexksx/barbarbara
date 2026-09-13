from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator, Field, Tag


class CurdlesBelowResponse(BaseModel):
    type: Literal["curdles_below"] = "curdles_below"
    ph: float = Field(ge=0.0, le=14.0)


class MaxAbvResponse(BaseModel):
    type: Literal["max_abv"] = "max_abv"
    abv: float = Field(ge=0.0, le=1.0)


def _constraint_discriminator(value: dict[str, object]) -> str:
    return str(value.get("type", ""))


type ConstraintResponse = Annotated[
    Annotated[CurdlesBelowResponse, Tag("curdles_below")]
    | Annotated[MaxAbvResponse, Tag("max_abv")],
    Discriminator(_constraint_discriminator),
]
