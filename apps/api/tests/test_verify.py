from fastapi.testclient import TestClient


def _gimlet_request() -> dict[str, object]:
    return {
        "actions": [
            {"type": "add", "material_id": "vodka", "volume_ml": 60.0, "equipment_id": "shaker"},
            {"type": "add", "material_id": "lime", "volume_ml": 30.0, "equipment_id": "shaker"},
            {"type": "add", "material_id": "syrup", "volume_ml": 15.0, "equipment_id": "shaker"},
            {"type": "pour", "from_equipment_id": "shaker", "to_equipment_id": "glass"},
        ],
        "materials": {
            "vodka": {
                "id": "vodka",
                "properties": {"ph": 6.0, "brix": 0.0, "abv": 0.4, "density": 0.94},
                "tags": ["spirit", "liquid"],
            },
            "lime": {
                "id": "lime",
                "properties": {"ph": 2.0, "brix": 8.0, "abv": 0.0, "density": 1.03},
                "tags": ["citrus", "liquid"],
            },
            "syrup": {
                "id": "syrup",
                "properties": {"ph": 7.0, "brix": 50.0, "abv": 0.0, "density": 1.33},
                "tags": ["sweetener", "liquid"],
            },
        },
        "equipment": {
            "shaker": {"id": "shaker", "capacity_ml": 500.0, "accepts_tags": ["liquid"]},
            "glass": {"id": "glass", "capacity_ml": 300.0, "accepts_tags": ["liquid"]},
        },
    }


def test_valid_plan_returns_200(client: TestClient) -> None:
    response = client.post("/verify", json=_gimlet_request())
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["violations"] == []


def test_valid_plan_returns_equipment_states(client: TestClient) -> None:
    response = client.post("/verify", json=_gimlet_request())
    body = response.json()
    assert "glass" in body["equipment_states"]
    glass = body["equipment_states"]["glass"]
    assert glass["contents"] is not None
    assert glass["contents"]["total_volume_ml"] == 105.0


def test_capacity_exceeded(client: TestClient) -> None:
    payload = {
        "actions": [
            {"type": "add", "material_id": "vodka", "volume_ml": 60.0, "equipment_id": "tiny"},
        ],
        "materials": {
            "vodka": {
                "id": "vodka",
                "properties": {"ph": 6.0, "brix": 0.0, "abv": 0.4, "density": 0.94},
                "tags": ["liquid"],
            },
        },
        "equipment": {
            "tiny": {"id": "tiny", "capacity_ml": 30.0, "accepts_tags": ["liquid"]},
        },
    }
    response = client.post("/verify", json=payload)
    body = response.json()
    assert body["valid"] is False
    assert any(v["kind"] == "capacity_exceeded" for v in body["violations"])


def test_constraint_violated(client: TestClient) -> None:
    payload = {
        "actions": [
            {"type": "add", "material_id": "cream", "volume_ml": 30.0, "equipment_id": "shaker"},
            {"type": "add", "material_id": "lime", "volume_ml": 90.0, "equipment_id": "shaker"},
        ],
        "materials": {
            "cream": {
                "id": "cream",
                "properties": {"ph": 6.5, "brix": 3.0, "abv": 0.0, "density": 1.01},
                "tags": ["dairy", "liquid"],
                "constraints": [{"type": "curdles_below", "ph": 4.6}],
            },
            "lime": {
                "id": "lime",
                "properties": {"ph": 2.0, "brix": 8.0, "abv": 0.0, "density": 1.03},
                "tags": ["citrus", "liquid"],
            },
        },
        "equipment": {
            "shaker": {"id": "shaker", "capacity_ml": 500.0, "accepts_tags": []},
        },
    }
    response = client.post("/verify", json=payload)
    body = response.json()
    assert body["valid"] is False
    assert any(v["kind"] == "constraint_violated" for v in body["violations"])


def test_material_not_found(client: TestClient) -> None:
    payload = {
        "actions": [
            {"type": "add", "material_id": "ghost", "volume_ml": 30.0, "equipment_id": "shaker"},
        ],
        "materials": {},
        "equipment": {
            "shaker": {"id": "shaker", "capacity_ml": 500.0, "accepts_tags": []},
        },
    }
    response = client.post("/verify", json=payload)
    body = response.json()
    assert body["valid"] is False
    assert body["violations"][0]["kind"] == "material_not_found"


def test_strain_action(client: TestClient) -> None:
    payload = {
        "actions": [
            {"type": "add", "material_id": "water", "volume_ml": 100.0, "equipment_id": "tin"},
            {"type": "add", "material_id": "mint", "volume_ml": 10.0, "equipment_id": "tin"},
            {
                "type": "strain",
                "from_equipment_id": "tin",
                "to_equipment_id": "glass",
                "remove_tags": ["solid"],
            },
        ],
        "materials": {
            "water": {
                "id": "water",
                "properties": {"ph": 7.0, "brix": 0.0, "abv": 0.0, "density": 1.0},
                "tags": ["liquid"],
            },
            "mint": {
                "id": "mint",
                "properties": {"ph": 6.0, "brix": 0.0, "abv": 0.0, "density": 0.9},
                "tags": ["solid", "herb"],
            },
        },
        "equipment": {
            "tin": {"id": "tin", "capacity_ml": 500.0, "accepts_tags": []},
            "glass": {"id": "glass", "capacity_ml": 300.0, "accepts_tags": []},
        },
    }
    response = client.post("/verify", json=payload)
    body = response.json()
    assert body["valid"] is True
    assert body["equipment_states"]["glass"]["contents"]["total_volume_ml"] == 100.0


def test_invalid_request_returns_422(client: TestClient) -> None:
    response = client.post("/verify", json={"actions": "not a list"})
    assert response.status_code == 422
