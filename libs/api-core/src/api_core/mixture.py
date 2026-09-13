from __future__ import annotations

from dataclasses import dataclass

from api_core.constraint import Violation
from api_core.material import Material
from api_core.properties import Properties, mix_properties


@dataclass(frozen=True, slots=True)
class MixtureComponent:
    material: Material
    volume_ml: float


@dataclass(frozen=True, slots=True)
class Mixture:
    components: tuple[MixtureComponent, ...] = ()

    @property
    def total_volume_ml(self) -> float:
        return sum(c.volume_ml for c in self.components)

    @property
    def properties(self) -> Properties | None:
        if not self.components:
            return None
        return mix_properties([(c.material.properties, c.volume_ml) for c in self.components])

    def add(self, material: Material, volume_ml: float) -> Mixture:
        return Mixture(components=(*self.components, MixtureComponent(material, volume_ml)))

    def combine(self, other: Mixture) -> Mixture:
        return Mixture(components=self.components + other.components)

    def strain(self, remove_tags: frozenset[str]) -> Mixture:
        kept = tuple(c for c in self.components if not c.material.tags & remove_tags)
        return Mixture(components=kept)

    def check_constraints(self) -> list[Violation]:
        props = self.properties
        if props is None:
            return []
        violations: list[Violation] = []
        for component in self.components:
            for constraint in component.material.constraints:
                violation = constraint.check(props)
                if violation is not None:
                    violations.append(violation)
        return violations
