import pytest
from pydantic import ValidationError

from api_rest_contract.properties import PropertiesResponse


def test_valid_properties() -> None:
    props = PropertiesResponse(ph=7.0, brix=0.0, abv=0.0, density=1.0)
    assert props.ph == 7.0


def test_ph_out_of_range() -> None:
    with pytest.raises(ValidationError):
        PropertiesResponse(ph=-1.0, brix=0.0, abv=0.0, density=1.0)


def test_abv_out_of_range() -> None:
    with pytest.raises(ValidationError):
        PropertiesResponse(ph=7.0, brix=0.0, abv=1.5, density=1.0)


def test_density_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        PropertiesResponse(ph=7.0, brix=0.0, abv=0.0, density=0.0)
