from __future__ import annotations

from dataclasses import dataclass

from api_core.constraint import Constraint
from api_core.properties import Properties


@dataclass(frozen=True, slots=True)
class Material:
    id: str
    properties: Properties
    tags: frozenset[str]
    constraints: tuple[Constraint, ...] = ()
