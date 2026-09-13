from fastapi.testclient import TestClient


def _shaker_payload() -> dict[str, object]:
    return {
        "id": "shaker",
        "capacity_ml": 500.0,
        "accepts_tags": ["liquid"],
    }


def test_create_equipment(client: TestClient) -> None:
    response = client.post("/equipment", json=_shaker_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == "shaker"
    assert body["capacity_ml"] == 500.0


def test_list_equipment(client: TestClient) -> None:
    client.post("/equipment", json=_shaker_payload())
    client.post(
        "/equipment", json={"id": "glass", "capacity_ml": 300.0, "accepts_tags": ["liquid"]}
    )
    response = client.get("/equipment")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_equipment_by_id(client: TestClient) -> None:
    client.post("/equipment", json=_shaker_payload())
    response = client.get("/equipment/shaker")
    assert response.status_code == 200
    assert response.json()["id"] == "shaker"


def test_get_equipment_not_found(client: TestClient) -> None:
    response = client.get("/equipment/ghost")
    assert response.status_code == 404


def test_delete_equipment(client: TestClient) -> None:
    client.post("/equipment", json=_shaker_payload())
    response = client.delete("/equipment/shaker")
    assert response.status_code == 204
    assert client.get("/equipment/shaker").status_code == 404


def test_delete_equipment_not_found(client: TestClient) -> None:
    response = client.delete("/equipment/ghost")
    assert response.status_code == 404
