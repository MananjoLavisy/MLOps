from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import joblib


DEFAULT_FEATURE_COUNT = 7


def get_model_path() -> Path:
    return Path(os.getenv("MODEL_PATH", "models/model.joblib"))


def get_metadata_path(model_path: Path | None = None) -> Path:
    resolved_model_path = model_path or get_model_path()
    return resolved_model_path.with_suffix(".json")


def load_model(model_path: Path | None = None):
    resolved_model_path = model_path or get_model_path()
    if not resolved_model_path.exists():
        raise FileNotFoundError(
            "Model file not found at "
            f"{resolved_model_path}. Run `python -m src.train` first."
        )
    return joblib.load(resolved_model_path)


def load_metadata(model_path: Path | None = None) -> dict[str, Any]:
    metadata_path = get_metadata_path(model_path)
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def get_expected_feature_count(model_path: Path | None = None) -> int:
    metadata = load_metadata(model_path)
    return int(metadata.get("feature_count", DEFAULT_FEATURE_COUNT))


def get_feature_names(model_path: Path | None = None) -> list[str]:
    metadata = load_metadata(model_path)
    feature_names = metadata.get("feature_names")
    if isinstance(feature_names, list):
        return [str(name) for name in feature_names]
    return []


def run_prediction(
    features: list[float], model_path: Path | None = None
) -> dict[str, Any]:
    model = load_model(model_path)
    prediction = model.predict([features])[0]
    result: dict[str, Any] = {"prediction": str(prediction)}

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([features])[0]
        best_index, best_probability = max(
            enumerate(probabilities), key=lambda item: item[1]
        )
        result["confidence"] = round(float(best_probability), 4)
        if hasattr(model, "classes_"):
            result["predicted_class"] = str(model.classes_[best_index])

    return result
