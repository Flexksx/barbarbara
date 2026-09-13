from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Properties:
    ph: float
    brix: float
    abv: float
    density: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.ph <= 14.0:
            msg = f"pH must be between 0 and 14, got {self.ph}"
            raise ValueError(msg)
        if not 0.0 <= self.abv <= 1.0:
            msg = f"ABV must be between 0 and 1, got {self.abv}"
            raise ValueError(msg)
        if self.brix < 0.0:
            msg = f"Brix must be non-negative, got {self.brix}"
            raise ValueError(msg)
        if self.density <= 0.0:
            msg = f"Density must be positive, got {self.density}"
            raise ValueError(msg)


def mix_properties(components: list[tuple[Properties, float]]) -> Properties:
    if not components:
        msg = "Cannot mix zero components"
        raise ValueError(msg)

    total_volume = sum(vol for _, vol in components)
    if total_volume <= 0:
        msg = "Total volume must be positive"
        raise ValueError(msg)

    weighted_h_plus = sum(vol * (10.0 ** (-p.ph)) for p, vol in components)
    mixed_ph = -math.log10(weighted_h_plus / total_volume)

    mixed_brix = sum(vol * p.brix for p, vol in components) / total_volume
    mixed_abv = sum(vol * p.abv for p, vol in components) / total_volume

    total_mass = sum(vol * p.density for p, vol in components)
    mixed_density = total_mass / total_volume

    return Properties(
        ph=mixed_ph,
        brix=mixed_brix,
        abv=mixed_abv,
        density=mixed_density,
    )
