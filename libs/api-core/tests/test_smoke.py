from collections.abc import Callable

from api_core.action import Add, Pour
from api_core.equipment import Equipment
from api_core.material import Material
from api_core.verification import verify


def test_gimlet_valid(bar_registry: tuple[dict[str, Material], dict[str, Equipment]]) -> None:
    materials, equipment = bar_registry
    actions = [
        Add(material_id="vodka", volume_ml=60.0, equipment_id="shaker"),
        Add(material_id="lime_juice", volume_ml=30.0, equipment_id="shaker"),
        Add(material_id="simple_syrup", volume_ml=15.0, equipment_id="shaker"),
        Pour(from_equipment_id="shaker", to_equipment_id="glass"),
    ]
    result = verify(actions, materials, equipment)
    assert result.valid
    assert result.violations == ()


def test_cream_curdles_with_acid(
    bar_registry: tuple[dict[str, Material], dict[str, Equipment]],
) -> None:
    materials, equipment = bar_registry
    actions = [
        Add(material_id="cream", volume_ml=60.0, equipment_id="shaker"),
        Add(material_id="lime_juice", volume_ml=60.0, equipment_id="shaker"),
    ]
    result = verify(actions, materials, equipment)
    assert not result.valid
    assert any(v.kind == "constraint_violated" for v in result.violations)


def test_overflow_rejected(
    bar_registry: tuple[dict[str, Material], dict[str, Equipment]],
    make_equipment: Callable[..., Equipment],
) -> None:
    materials, _ = bar_registry
    tiny = make_equipment("tiny", capacity_ml=30.0)
    actions = [Add(material_id="vodka", volume_ml=60.0, equipment_id="tiny")]
    result = verify(actions, materials, {"tiny": tiny})
    assert not result.valid
    assert any(v.kind == "capacity_exceeded" for v in result.violations)
