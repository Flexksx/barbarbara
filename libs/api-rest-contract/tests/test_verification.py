from api_rest_contract.verification import StepViolationResponse, VerifyPlanResponse


def test_response_serialization() -> None:
    response = VerifyPlanResponse(
        valid=False,
        violations=[
            StepViolationResponse(step=2, kind="constraint_violated", message="pH too low"),
        ],
        equipment_states={
            "shaker": {  # type: ignore[dict-item]
                "id": "shaker",
                "capacity_ml": 500.0,
                "accepts_tags": ["liquid"],
            },
        },
    )
    data = response.model_dump()
    assert data["valid"] is False
    assert len(data["violations"]) == 1
    assert data["violations"][0]["kind"] == "constraint_violated"


def test_response_roundtrip() -> None:
    raw = {
        "valid": True,
        "violations": [],
        "equipment_states": {
            "glass": {
                "id": "glass",
                "capacity_ml": 300.0,
                "accepts_tags": ["liquid"],
                "contents": {
                    "components": [{"material_id": "vodka", "volume_ml": 60.0}],
                    "total_volume_ml": 60.0,
                    "properties": {"ph": 6.0, "brix": 0.0, "abv": 0.4, "density": 0.94},
                },
            },
        },
    }
    response = VerifyPlanResponse.model_validate(raw)
    assert response.valid
    assert response.equipment_states["glass"].contents is not None
    assert response.equipment_states["glass"].contents.total_volume_ml == 60.0
