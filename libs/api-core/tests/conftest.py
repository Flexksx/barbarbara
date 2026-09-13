from collections.abc import Callable

import pytest

from api_core.constraint import CurdlesBelow
from api_core.equipment import Equipment
from api_core.material import Material
from api_core.properties import Properties

type MaterialFactory = Callable[..., Material]
type EquipmentFactory = Callable[..., Equipment]


def make_material_fn(
    material_id: str,
    *,
    ph: float = 7.0,
    abv: float = 0.0,
    brix: float = 0.0,
    density: float = 1.0,
    tags: frozenset[str] | None = None,
    constraints: tuple[object, ...] = (),
) -> Material:
    return Material(
        id=material_id,
        properties=Properties(ph=ph, brix=brix, abv=abv, density=density),
        tags=tags if tags is not None else frozenset({"liquid"}),
        constraints=constraints,  # type: ignore[arg-type]
    )


def make_equipment_fn(
    equipment_id: str,
    *,
    capacity_ml: float = 500.0,
    accepts_tags: frozenset[str] | None = None,
) -> Equipment:
    return Equipment(
        id=equipment_id,
        capacity_ml=capacity_ml,
        accepts_tags=accepts_tags if accepts_tags is not None else frozenset({"liquid"}),
    )


@pytest.fixture
def make_material() -> MaterialFactory:
    return make_material_fn


@pytest.fixture
def make_equipment() -> EquipmentFactory:
    return make_equipment_fn


@pytest.fixture
def bar_registry() -> tuple[dict[str, Material], dict[str, Equipment]]:
    m = make_material_fn
    vodka = m("vodka", ph=6.0, abv=0.40, density=0.94)
    lime_juice = m(
        "lime_juice", ph=2.0, brix=8.0, density=1.03, tags=frozenset({"citrus", "acidic", "liquid"})
    )
    simple_syrup = m(
        "simple_syrup", ph=7.0, brix=50.0, density=1.33, tags=frozenset({"sweetener", "liquid"})
    )
    cream = m(
        "cream",
        ph=6.5,
        brix=3.0,
        density=1.01,
        tags=frozenset({"dairy", "liquid"}),
        constraints=(CurdlesBelow(ph=4.6),),
    )
    materials = {mat.id: mat for mat in [vodka, lime_juice, simple_syrup, cream]}

    e = make_equipment_fn
    shaker = e("shaker")
    glass = e("glass", capacity_ml=300.0)
    equipment = {eq.id: eq for eq in [shaker, glass]}

    return materials, equipment
