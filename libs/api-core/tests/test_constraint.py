from api_core.constraint import CurdlesBelow, MaxAbv
from api_core.properties import Properties


def test_curdles_below_safe_ph() -> None:
    constraint = CurdlesBelow(ph=4.6)
    props = Properties(ph=5.0, brix=0.0, abv=0.0, density=1.0)
    assert constraint.check(props) is None


def test_curdles_below_exact_threshold_is_safe() -> None:
    constraint = CurdlesBelow(ph=4.6)
    props = Properties(ph=4.6, brix=0.0, abv=0.0, density=1.0)
    assert constraint.check(props) is None


def test_curdles_below_violates() -> None:
    constraint = CurdlesBelow(ph=4.6)
    props = Properties(ph=3.0, brix=0.0, abv=0.0, density=1.0)
    violation = constraint.check(props)
    assert violation is not None
    assert violation.constraint == "curdles_below"


def test_max_abv_below_is_safe() -> None:
    constraint = MaxAbv(abv=0.5)
    props = Properties(ph=7.0, brix=0.0, abv=0.3, density=1.0)
    assert constraint.check(props) is None


def test_max_abv_exact_is_safe() -> None:
    constraint = MaxAbv(abv=0.5)
    props = Properties(ph=7.0, brix=0.0, abv=0.5, density=1.0)
    assert constraint.check(props) is None


def test_max_abv_above_violates() -> None:
    constraint = MaxAbv(abv=0.5)
    props = Properties(ph=7.0, brix=0.0, abv=0.6, density=1.0)
    violation = constraint.check(props)
    assert violation is not None
    assert violation.constraint == "max_abv"
