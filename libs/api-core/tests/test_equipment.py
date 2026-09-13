from collections.abc import Callable

import pytest

from api_core.equipment import Equipment
from api_core.material import Material


def test_empty_accepts_tags_means_accept_all(make_material: Callable[..., Material]) -> None:
    eq = Equipment(id="bowl", capacity_ml=500.0, accepts_tags=frozenset())
    assert eq.can_accept(make_material("water", tags=frozenset({"liquid"})))
    assert eq.can_accept(make_material("ice", tags=frozenset({"solid"})))


def test_tag_filter(make_material: Callable[..., Material]) -> None:
    eq = Equipment(id="glass", capacity_ml=300.0, accepts_tags=frozenset({"liquid"}))
    assert eq.can_accept(make_material("water", tags=frozenset({"liquid"})))
    assert not eq.can_accept(make_material("ice", tags=frozenset({"solid"})))


def test_remaining_capacity() -> None:
    eq = Equipment(id="glass", capacity_ml=300.0, accepts_tags=frozenset())
    assert eq.remaining_capacity_ml() == pytest.approx(300.0)


def test_remaining_after_add(make_material: Callable[..., Material]) -> None:
    eq = Equipment(id="glass", capacity_ml=300.0, accepts_tags=frozenset())
    eq = eq.add(make_material("water"), 100.0)
    assert eq.remaining_capacity_ml() == pytest.approx(200.0)


def test_pour_empties_source_fills_target(make_material: Callable[..., Material]) -> None:
    water = make_material("water")
    source = Equipment(id="shaker", capacity_ml=500.0, accepts_tags=frozenset()).add(water, 100.0)
    target = Equipment(id="glass", capacity_ml=300.0, accepts_tags=frozenset())
    emptied, filled = source.pour_into(target)
    assert emptied.contents.total_volume_ml == pytest.approx(0.0)
    assert filled.contents.total_volume_ml == pytest.approx(100.0)


def test_strain_keeps_liquids_removes_solids(make_material: Callable[..., Material]) -> None:
    water = make_material("water", tags=frozenset({"liquid"}))
    ice = make_material("ice", tags=frozenset({"solid"}))
    shaker = Equipment(id="shaker", capacity_ml=500.0, accepts_tags=frozenset())
    shaker = shaker.add(water, 100.0).add(ice, 50.0)
    glass = Equipment(id="glass", capacity_ml=300.0, accepts_tags=frozenset())
    emptied, filled = shaker.strain_into(glass, frozenset({"solid"}))
    assert emptied.contents.total_volume_ml == pytest.approx(0.0)
    assert filled.contents.total_volume_ml == pytest.approx(100.0)
