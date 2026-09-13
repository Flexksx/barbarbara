from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Add:
    material_id: str
    volume_ml: float
    equipment_id: str


@dataclass(frozen=True, slots=True)
class Pour:
    from_equipment_id: str
    to_equipment_id: str


@dataclass(frozen=True, slots=True)
class Strain:
    from_equipment_id: str
    to_equipment_id: str
    remove_tags: frozenset[str]


type Action = Add | Pour | Strain
