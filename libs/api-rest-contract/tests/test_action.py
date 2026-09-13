from api_rest_contract.action import AddActionResponse, PourActionResponse, StrainActionResponse
from api_rest_contract.verification import VerifyPlanRequest


def test_add_action_serialization() -> None:
    action = AddActionResponse(material_id="vodka", volume_ml=60.0, equipment_id="shaker")
    data = action.model_dump()
    assert data["type"] == "add"
    assert data["material_id"] == "vodka"


def test_pour_action_serialization() -> None:
    action = PourActionResponse(from_equipment_id="shaker", to_equipment_id="glass")
    data = action.model_dump()
    assert data["type"] == "pour"


def test_strain_action_serialization() -> None:
    action = StrainActionResponse(
        from_equipment_id="tin",
        to_equipment_id="glass",
        remove_tags=frozenset({"solid"}),
    )
    data = action.model_dump()
    assert data["type"] == "strain"
    assert "solid" in data["remove_tags"]


def test_action_discriminator_in_request() -> None:
    raw = {
        "actions": [
            {"type": "add", "material_id": "vodka", "volume_ml": 60.0, "equipment_id": "shaker"},
            {"type": "pour", "from_equipment_id": "shaker", "to_equipment_id": "glass"},
        ],
        "materials": {
            "vodka": {
                "id": "vodka",
                "properties": {"ph": 6.0, "brix": 0.0, "abv": 0.4, "density": 0.94},
                "tags": ["spirit", "liquid"],
            },
        },
        "equipment": {
            "shaker": {"id": "shaker", "capacity_ml": 500.0, "accepts_tags": ["liquid"]},
            "glass": {"id": "glass", "capacity_ml": 300.0, "accepts_tags": ["liquid"]},
        },
    }
    request = VerifyPlanRequest.model_validate(raw)
    assert len(request.actions) == 2
    assert isinstance(request.actions[0], AddActionResponse)
    assert isinstance(request.actions[1], PourActionResponse)
