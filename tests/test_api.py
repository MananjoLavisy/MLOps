from fastapi.testclient import TestClient

from src.app import app
from src.train import train_model


def build_valid_payload() -> dict[str, float]:
    return {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87974371,
        "humidity": 82.00274423,
        "ph": 6.502985292000001,
        "rainfall": 202.9355362,
    }


def test_healthcheck() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "expected_feature_count" in body
    assert body["expected_feature_count"] == 7


def test_model_info_without_model(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("MODEL_PATH", str(tmp_path / "missing.joblib"))
    client = TestClient(app)

    response = client.get("/model-info")

    assert response.status_code == 200
    body = response.json()
    assert body["model_loaded"] is False
    assert body["dataset_name"] is None


def test_predict_returns_prediction(tmp_path, monkeypatch) -> None:
    model_path = tmp_path / "model.joblib"
    train_model(model_path)
    monkeypatch.setenv("MODEL_PATH", str(model_path))

    client = TestClient(app)

    response = client.post("/predict", json=build_valid_payload())

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["recommended_crop"], str)
    assert 0 <= body["confidence"] <= 1


def test_predict_rejects_invalid_payload() -> None:
    client = TestClient(app)
    payload = build_valid_payload()
    payload.pop("rainfall")
    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_model_info_returns_metadata(tmp_path, monkeypatch) -> None:
    model_path = tmp_path / "model.joblib"
    train_model(model_path)
    monkeypatch.setenv("MODEL_PATH", str(model_path))

    client = TestClient(app)
    response = client.get("/model-info")

    assert response.status_code == 200
    body = response.json()
    assert body["dataset_name"] == "Crop_recommendation"
    assert body["feature_count"] == 7
    assert "rice" in body["classes"]


def test_predict_returns_503_when_model_is_missing(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("MODEL_PATH", str(tmp_path / "missing.joblib"))

    client = TestClient(app)
    response = client.post("/predict", json=build_valid_payload())

    assert response.status_code == 503
