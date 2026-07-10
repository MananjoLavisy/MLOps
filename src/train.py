from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from src.model_artifacts import get_metadata_path, get_model_path

DEFAULT_MODEL_PATH = get_model_path()
DEFAULT_DATASET_PATH = Path(os.getenv("DATASET_PATH", "data/Crop_recommendation.csv"))
FEATURE_NAMES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET_NAME = "label"


def load_dataset(
    dataset_path: Path = DEFAULT_DATASET_PATH,
) -> tuple[list[list[float]], list[str]]:
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file not found at {dataset_path}.")

    features: list[list[float]] = []
    labels: list[str] = []
    with dataset_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            features.append([float(row[name]) for name in FEATURE_NAMES])
            labels.append(str(row[TARGET_NAME]))

    return features, labels


def train_model(
    output_path: Path = DEFAULT_MODEL_PATH,
    dataset_path: Path = DEFAULT_DATASET_PATH,
) -> dict[str, float | int | str | list[str]]:
    features, labels = load_dataset(dataset_path)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    metrics = {
        "dataset_name": dataset_path.stem,
        "target_name": TARGET_NAME,
        "problem_type": "classification",
        "feature_count": len(FEATURE_NAMES),
        "feature_names": FEATURE_NAMES,
        "classes": [str(label) for label in model.classes_],
        "sample_count": len(features),
        "accuracy": round(accuracy_score(y_test, predictions), 4),
        "f1_score": round(f1_score(y_test, predictions, average="macro"), 4),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    get_metadata_path(output_path).write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    return metrics


if __name__ == "__main__":
    result = train_model()
    print(json.dumps(result, indent=2))
