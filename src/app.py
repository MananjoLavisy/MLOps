from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

from src.model_artifacts import (
    get_expected_feature_count,
    get_feature_names,
    get_model_path,
    load_metadata,
    run_prediction,
)


class CropRecommendationRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

    def to_feature_vector(self) -> list[float]:
        return [
            self.N,
            self.P,
            self.K,
            self.temperature,
            self.humidity,
            self.ph,
            self.rainfall,
        ]


app = FastAPI(title="MLOps FastAPI Service", version="0.1.0")
Instrumentator().instrument(app).expose(app)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "mlops-fastapi",
        "version": app.version,
        "docs": "/docs",
    }


@app.get("/health")
def healthcheck() -> dict[str, bool | int | list[str]]:
    model_path = get_model_path()
    return {
        "status": True,
        "model_loaded": model_path.exists(),
        "expected_feature_count": get_expected_feature_count(model_path),
        "feature_names": get_feature_names(model_path),
    }


@app.get("/model-info")
def model_info() -> dict[str, Any]:
    model_path = get_model_path()
    metadata = load_metadata(model_path)
    return {
        "model_path": str(model_path),
        "model_loaded": model_path.exists(),
        "dataset_name": metadata.get("dataset_name"),
        "feature_count": metadata.get("feature_count"),
        "feature_names": metadata.get("feature_names"),
        "classes": metadata.get("classes"),
    }


@app.post("/predict")
def predict(payload: CropRecommendationRequest) -> dict[str, str | float]:
    try:
        result = run_prediction(payload.to_feature_vector())
        return {
            "recommended_crop": str(result["prediction"]),
            "confidence": float(result.get("confidence", 0.0)),
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
