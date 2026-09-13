from fastapi.testclient import TestClient


def _vodka_payload() -> dict[str, object]:
    return {
        "id": "vodka",
        "properties": {"ph": 6.0, "brix": 0.0, "abv": 0.4, "density": 0.94},
        "tags": ["spirit", "liquid"],
    }


def _cream_payload() -> dict[str, object]:
    return {
        "id": "cream",
        "properties": {"ph": 6.5, "brix": 3.0, "abv": 0.0, "density": 1.01},
        "tags": ["dairy", "liquid"],
        "constraints": [{"type": "curdles_below", "ph": 4.6}],
    }


def test_create_material(client: TestClient) -> None:
    response = client.post("/materials", json=_vodka_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == "vodka"
    assert body["properties"]["abv"] == 0.4


def test_create_material_with_constraints(client: TestClient) -> None:
    response = client.post("/materials", json=_cream_payload())
    assert response.status_code == 201
    body = response.json()
    assert len(body["constraints"]) == 1
    assert body["constraints"][0]["type"] == "curdles_below"


def test_list_materials(client: TestClient) -> None:
    client.post("/materials", json=_vodka_payload())
    client.post("/materials", json=_cream_payload())
    response = client.get("/materials")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_material_by_id(client: TestClient) -> None:
    client.post("/materials", json=_vodka_payload())
    response = client.get("/materials/vodka")
    assert response.status_code == 200
    assert response.json()["id"] == "vodka"


def test_get_material_not_found(client: TestClient) -> None:
    response = client.get("/materials/ghost")
    assert response.status_code == 404


def test_delete_material(client: TestClient) -> None:
    client.post("/materials", json=_vodka_payload())
    response = client.delete("/materials/vodka")
    assert response.status_code == 204
    assert client.get("/materials/vodka").status_code == 404


def test_delete_material_not_found(client: TestClient) -> None:
    response = client.delete("/materials/ghost")
    assert response.status_code == 404
