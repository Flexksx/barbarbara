import pytest

from api_core.properties import Properties, mix_properties


def test_valid_properties() -> None:
    p = Properties(ph=7.0, brix=0.0, abv=0.0, density=1.0)
    assert p.ph == 7.0


def test_ph_below_zero() -> None:
    with pytest.raises(ValueError, match="pH"):
        Properties(ph=-1.0, brix=0.0, abv=0.0, density=1.0)


def test_ph_above_fourteen() -> None:
    with pytest.raises(ValueError, match="pH"):
        Properties(ph=15.0, brix=0.0, abv=0.0, density=1.0)


def test_abv_negative() -> None:
    with pytest.raises(ValueError, match="ABV"):
        Properties(ph=7.0, brix=0.0, abv=-0.1, density=1.0)


def test_abv_above_one() -> None:
    with pytest.raises(ValueError, match="ABV"):
        Properties(ph=7.0, brix=0.0, abv=1.1, density=1.0)


def test_brix_negative() -> None:
    with pytest.raises(ValueError, match="Brix"):
        Properties(ph=7.0, brix=-1.0, abv=0.0, density=1.0)


def test_density_zero() -> None:
    with pytest.raises(ValueError, match=r"[Dd]ensity"):
        Properties(ph=7.0, brix=0.0, abv=0.0, density=0.0)


def test_properties_immutable() -> None:
    p = Properties(ph=7.0, brix=0.0, abv=0.0, density=1.0)
    with pytest.raises(AttributeError):
        p.ph = 3.0  # type: ignore[misc]


def test_mix_single_component_identity() -> None:
    p = Properties(ph=3.0, brix=10.0, abv=0.0, density=1.05)
    result = mix_properties([(p, 100.0)])
    assert result.ph == pytest.approx(3.0, abs=0.01)
    assert result.brix == pytest.approx(10.0)
    assert result.abv == pytest.approx(0.0)
    assert result.density == pytest.approx(1.05)


def test_mix_ph_is_logarithmic() -> None:
    acid = Properties(ph=2.0, brix=0.0, abv=0.0, density=1.0)
    mild = Properties(ph=4.0, brix=0.0, abv=0.0, density=1.0)
    result = mix_properties([(acid, 50.0), (mild, 50.0)])
    assert result.ph == pytest.approx(2.30, abs=0.01)


def test_mix_abv_dilution() -> None:
    spirit = Properties(ph=6.0, brix=0.0, abv=0.40, density=0.94)
    mixer = Properties(ph=7.0, brix=10.0, abv=0.0, density=1.05)
    result = mix_properties([(spirit, 60.0), (mixer, 120.0)])
    assert result.abv == pytest.approx(0.40 * 60.0 / 180.0)


def test_mix_brix_weighted_average() -> None:
    sweet = Properties(ph=7.0, brix=50.0, abv=0.0, density=1.33)
    water = Properties(ph=7.0, brix=0.0, abv=0.0, density=1.0)
    result = mix_properties([(sweet, 30.0), (water, 90.0)])
    assert result.brix == pytest.approx(50.0 * 30.0 / 120.0)


def test_mix_density_mass_weighted() -> None:
    heavy = Properties(ph=7.0, brix=0.0, abv=0.0, density=1.5)
    light = Properties(ph=7.0, brix=0.0, abv=0.0, density=1.0)
    result = mix_properties([(heavy, 50.0), (light, 50.0)])
    expected = (50.0 * 1.5 + 50.0 * 1.0) / 100.0
    assert result.density == pytest.approx(expected)


def test_mix_empty_raises() -> None:
    with pytest.raises(ValueError, match="zero"):
        mix_properties([])
