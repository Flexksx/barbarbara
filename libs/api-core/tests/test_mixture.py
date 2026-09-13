from collections.abc import Callable

import pytest

from api_core.constraint import CurdlesBelow
from api_core.material import Material
from api_core.mixture import Mixture


def test_empty_volume_is_zero() -> None:
    assert Mixture().total_volume_ml == 0.0


def test_empty_properties_is_none() -> None:
    assert Mixture().properties is None


def test_empty_no_constraints() -> None:
    assert Mixture().check_constraints() == []


def test_add_single(make_material: Callable[..., Material]) -> None:
    vodka = make_material("vodka", ph=6.0, abv=0.40)
    m = Mixture().add(vodka, 60.0)
    assert m.total_volume_ml == 60.0
    assert m.properties is not None
    assert m.properties.abv == pytest.approx(0.40)


def test_add_two_materials(make_material: Callable[..., Material]) -> None:
    vodka = make_material("vodka", abv=0.40)
    juice = make_material("juice", ph=3.0)
    m = Mixture().add(vodka, 60.0).add(juice, 30.0)
    assert m.total_volume_ml == 90.0
    assert len(m.components) == 2


def test_add_is_immutable(make_material: Callable[..., Material]) -> None:
    vodka = make_material("vodka")
    original = Mixture()
    _after_add = original.add(vodka, 60.0)
    assert original.total_volume_ml == 0.0


def test_combine_volumes_sum(make_material: Callable[..., Material]) -> None:
    vodka = make_material("vodka")
    juice = make_material("juice")
    m1 = Mixture().add(vodka, 60.0)
    m2 = Mixture().add(juice, 30.0)
    combined = m1.combine(m2)
    assert combined.total_volume_ml == 90.0
    assert len(combined.components) == 2


def test_strain_removes_tagged(make_material: Callable[..., Material]) -> None:
    liquid = make_material("water", tags=frozenset({"liquid"}))
    herb = make_material("mint", tags=frozenset({"solid", "herb"}))
    m = Mixture().add(liquid, 100.0).add(herb, 10.0)
    strained = m.strain(frozenset({"solid"}))
    assert strained.total_volume_ml == 100.0
    assert len(strained.components) == 1


def test_strain_keeps_non_matching(make_material: Callable[..., Material]) -> None:
    a = make_material("a", tags=frozenset({"liquid"}))
    b = make_material("b", tags=frozenset({"liquid"}))
    m = Mixture().add(a, 50.0).add(b, 50.0)
    strained = m.strain(frozenset({"solid"}))
    assert strained.total_volume_ml == 100.0


def test_constraint_passes_when_safe(make_material: Callable[..., Material]) -> None:
    cream = make_material("cream", ph=6.5, constraints=(CurdlesBelow(ph=4.6),))
    syrup = make_material("syrup", ph=7.0)
    m = Mixture().add(cream, 60.0).add(syrup, 60.0)
    assert m.check_constraints() == []


def test_constraint_fails_when_acidic(make_material: Callable[..., Material]) -> None:
    cream = make_material("cream", ph=6.5, constraints=(CurdlesBelow(ph=4.6),))
    lime = make_material("lime", ph=2.0)
    m = Mixture().add(cream, 30.0).add(lime, 90.0)
    violations = m.check_constraints()
    assert len(violations) > 0
    assert violations[0].constraint == "curdles_below"
