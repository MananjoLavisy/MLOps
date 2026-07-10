from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.model_artifacts import (
    get_feature_names,
    get_expected_feature_count,
    get_model_path,
    run_prediction,
)


DEFAULT_MODEL_PATH = get_model_path()


def predict(
    features: list[float], model_path: Path = DEFAULT_MODEL_PATH
) -> dict[str, object]:
    expected_feature_count = get_expected_feature_count(model_path)
    if len(features) != expected_feature_count:
        raise ValueError(
            f"Expected {expected_feature_count} features, received {len(features)}."
        )
    return run_prediction(features, model_path)


if __name__ == "__main__":
    feature_names = get_feature_names(DEFAULT_MODEL_PATH)
    feature_help = (
        f"Feature vector in this order: {', '.join(feature_names)}"
        if feature_names
        else "Feature vector"
    )
    parser = argparse.ArgumentParser(
        description="Run a prediction from the trained model"
    )
    parser.add_argument("features", nargs="+", type=float, help=feature_help)
    args = parser.parse_args()
    print(json.dumps(predict(args.features), indent=2))
