from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from api_core.properties import Properties


@dataclass(frozen=True, slots=True)
class Violation:
    constraint: str
    message: str


@runtime_checkable
class Constraint(Protocol):
    def check(self, properties: Properties) -> Violation | None: ...


@dataclass(frozen=True, slots=True)
class CurdlesBelow:
    ph: float

    def check(self, properties: Properties) -> Violation | None:
        if properties.ph < self.ph:
            return Violation(
                constraint="curdles_below",
                message=f"pH {properties.ph:.2f} is below curdling threshold {self.ph}",
            )
        return None


@dataclass(frozen=True, slots=True)
class MaxAbv:
    abv: float

    def check(self, properties: Properties) -> Violation | None:
        if properties.abv > self.abv:
            return Violation(
                constraint="max_abv",
                message=f"ABV {properties.abv:.2f} exceeds maximum {self.abv}",
            )
        return None
