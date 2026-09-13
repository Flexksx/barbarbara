from collections.abc import Callable

from api_core.action import Add, Pour, Strain
from api_core.constraint import CurdlesBelow
from api_core.equipment import Equipment
from api_core.material import Material
from api_core.verification import verify


def test_valid_gimlet(
    make_material: Callable[..., Material], make_equipment: Callable[..., Equipment]
) -> None:
    vodka = make_material("vodka", abv=0.40)
    lime = make_material("lime", ph=2.0)
    syrup = make_material("syrup")
    materials = {m.id: m for m in [vodka, lime, syrup]}

    shaker = make_equipment("shaker")
    glass = make_equipment("glass", capacity_ml=300.0)
    equipment = {e.id: e for e in [shaker, glass]}

    actions = [
        Add(material_id="vodka", volume_ml=60.0, equipment_id="shaker"),
        Add(material_id="lime", volume_ml=30.0, equipment_id="shaker"),
        Add(material_id="syrup", volume_ml=15.0, equipment_id="shaker"),
        Pour(from_equipment_id="shaker", to_equipment_id="glass"),
    ]

    result = verify(actions, materials, equipment)
    assert result.valid
    assert result.violations == ()


def test_strain_removes_solids(
    make_material: Callable[..., Material], make_equipment: Callable[..., Equipment]
) -> None:
    water = make_material("water", tags=frozenset({"liquid"}))
    mint = make_material("mint", tags=frozenset({"solid", "herb"}))
    materials = {m.id: m for m in [water, mint]}

    tin = make_equipment("tin", accepts_tags=frozenset())
    glass = make_equipment("glass", accepts_tags=frozenset())
    equipment = {e.id: e for e in [tin, glass]}

    actions = [
        Add(material_id="water", volume_ml=100.0, equipment_id="tin"),
        Add(material_id="mint", volume_ml=10.0, equipment_id="tin"),
        Strain(from_equipment_id="tin", to_equipment_id="glass", remove_tags=frozenset({"solid"})),
    ]

    result = verify(actions, materials, equipment)
    assert result.valid


def test_material_not_found(make_equipment: Callable[..., Equipment]) -> None:
    equipment = {"shaker": make_equipment("shaker")}
    actions = [Add(material_id="ghost", volume_ml=30.0, equipment_id="shaker")]
    result = verify(actions, {}, equipment)
    assert not result.valid
    assert result.violations[0].kind == "material_not_found"


def test_equipment_not_found(make_material: Callable[..., Material]) -> None:
    vodka = make_material("vodka")
    actions = [Add(material_id="vodka", volume_ml=30.0, equipment_id="ghost")]
    result = verify(actions, {"vodka": vodka}, {})
    assert not result.valid
    assert result.violations[0].kind == "equipment_not_found"


def test_overflow_on_add(
    make_material: Callable[..., Material], make_equipment: Callable[..., Equipment]
) -> None:
    vodka = make_material("vodka")
    tiny = make_equipment("tiny", capacity_ml=30.0)
    actions = [Add(material_id="vodka", volume_ml=60.0, equipment_id="tiny")]
    result = verify(actions, {"vodka": vodka}, {"tiny": tiny})
    assert not result.valid
    assert result.violations[0].kind == "capacity_exceeded"


def test_overflow_on_pour(
    make_material: Callable[..., Material], make_equipment: Callable[..., Equipment]
) -> None:
    water = make_material("water")
    big = make_equipment("big", capacity_ml=500.0, accepts_tags=frozenset())
    small = make_equipment("small", capacity_ml=30.0, accepts_tags=frozenset())
    equipment = {"big": big, "small": small}
    actions = [
        Add(material_id="water", volume_ml=100.0, equipment_id="big"),
        Pour(from_equipment_id="big", to_equipment_id="small"),
    ]
    result = verify(actions, {"water": water}, equipment)
    assert not result.valid
    assert any(v.kind == "capacity_exceeded" for v in result.violations)


def test_tag_not_accepted(
    make_material: Callable[..., Material], make_equipment: Callable[..., Equipment]
) -> None:
    ice = make_material("ice", tags=frozenset({"solid"}))
    glass = make_equipment("glass", accepts_tags=frozenset({"liquid"}))
    actions = [Add(material_id="ice", volume_ml=50.0, equipment_id="glass")]
    result = verify(actions, {"ice": ice}, {"glass": glass})
    assert not result.valid
    assert result.violations[0].kind == "tag_not_accepted"


def test_cream_curdles_with_acid(
    make_material: Callable[..., Material], make_equipment: Callable[..., Equipment]
) -> None:
    cream = make_material("cream", ph=6.5, constraints=(CurdlesBelow(ph=4.6),))
    lime = make_material("lime", ph=2.0)
    shaker = make_equipment("shaker", accepts_tags=frozenset())
    actions = [
        Add(material_id="cream", volume_ml=30.0, equipment_id="shaker"),
        Add(material_id="lime", volume_ml=90.0, equipment_id="shaker"),
    ]
    result = verify(actions, {"cream": cream, "lime": lime}, {"shaker": shaker})
    assert not result.valid
    assert any(v.kind == "constraint_violated" for v in result.violations)


def test_cream_safe_with_sweetener(
    make_material: Callable[..., Material], make_equipment: Callable[..., Equipment]
) -> None:
    cream = make_material("cream", ph=6.5, constraints=(CurdlesBelow(ph=4.6),))
    syrup = make_material("syrup", ph=7.0)
    shaker = make_equipment("shaker", accepts_tags=frozenset())
    actions = [
        Add(material_id="cream", volume_ml=60.0, equipment_id="shaker"),
        Add(material_id="syrup", volume_ml=60.0, equipment_id="shaker"),
    ]
    result = verify(actions, {"cream": cream, "syrup": syrup}, {"shaker": shaker})
    assert result.valid
