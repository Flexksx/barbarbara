from api_rest_contract.constraint import CurdlesBelowResponse, MaxAbvResponse
from api_rest_contract.material import MaterialResponse


def test_curdles_below_serialization() -> None:
    constraint = CurdlesBelowResponse(ph=4.6)
    data = constraint.model_dump()
    assert data == {"type": "curdles_below", "ph": 4.6}


def test_max_abv_serialization() -> None:
    constraint = MaxAbvResponse(abv=0.5)
    data = constraint.model_dump()
    assert data == {"type": "max_abv", "abv": 0.5}


def test_constraint_discriminator_in_material() -> None:
    raw = {
        "id": "cream",
        "properties": {"ph": 6.5, "brix": 3.0, "abv": 0.0, "density": 1.01},
        "tags": ["dairy", "liquid"],
        "constraints": [{"type": "curdles_below", "ph": 4.6}],
    }
    material = MaterialResponse.model_validate(raw)
    assert len(material.constraints) == 1
    assert isinstance(material.constraints[0], CurdlesBelowResponse)
