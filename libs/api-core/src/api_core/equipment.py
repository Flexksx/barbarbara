from __future__ import annotations

from dataclasses import dataclass, field

from api_core.material import Material
from api_core.mixture import Mixture


@dataclass(frozen=True, slots=True)
class Equipment:
    id: str
    capacity_ml: float
    accepts_tags: frozenset[str]
    contents: Mixture = field(default_factory=Mixture)

    def can_accept(self, material: Material) -> bool:
        if not self.accepts_tags:
            return True
        return bool(material.tags & self.accepts_tags)

    def remaining_capacity_ml(self) -> float:
        return self.capacity_ml - self.contents.total_volume_ml

    def add(self, material: Material, volume_ml: float) -> Equipment:
        return Equipment(
            id=self.id,
            capacity_ml=self.capacity_ml,
            accepts_tags=self.accepts_tags,
            contents=self.contents.add(material, volume_ml),
        )

    def pour_into(self, other: Equipment) -> tuple[Equipment, Equipment]:
        emptied = Equipment(
            id=self.id,
            capacity_ml=self.capacity_ml,
            accepts_tags=self.accepts_tags,
            contents=Mixture(),
        )
        filled = Equipment(
            id=other.id,
            capacity_ml=other.capacity_ml,
            accepts_tags=other.accepts_tags,
            contents=other.contents.combine(self.contents),
        )
        return emptied, filled

    def strain_into(
        self, other: Equipment, remove_tags: frozenset[str]
    ) -> tuple[Equipment, Equipment]:
        strained = self.contents.strain(remove_tags)
        emptied = Equipment(
            id=self.id,
            capacity_ml=self.capacity_ml,
            accepts_tags=self.accepts_tags,
            contents=Mixture(),
        )
        filled = Equipment(
            id=other.id,
            capacity_ml=other.capacity_ml,
            accepts_tags=other.accepts_tags,
            contents=other.contents.combine(strained),
        )
        return emptied, filled
