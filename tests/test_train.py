from pathlib import Path

import json

from src.train import FEATURE_NAMES, train_model


def test_train_model_creates_artifacts(tmp_path: Path) -> None:
    model_path = tmp_path / "model.joblib"

    metrics = train_model(model_path)

    assert model_path.exists()
    assert model_path.with_suffix(".json").exists()
    metadata = json.loads(model_path.with_suffix(".json").read_text(encoding="utf-8"))
    assert metadata["dataset_name"] == "Crop_recommendation"
    assert metadata["feature_count"] == len(FEATURE_NAMES)
    assert metadata["feature_names"] == FEATURE_NAMES
    assert "rice" in metadata["classes"]
    assert metrics["accuracy"] > 0.9
    assert metrics["f1_score"] > 0.9
