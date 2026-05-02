"""Prediction model endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from app.models_loader import ModelsLoader
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/prediction", tags=["Prediction"])
loader = ModelsLoader()


class PredictionRequest(BaseModel):
    """Request model for predictions."""
    model_name: str
    features: Dict[str, Any]
    model_type: str = "classification"  # classification, regression, clustering


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    prediction: Any
    confidence: float = None
    model_name: str
    model_type: str


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> Dict[str, Any]:
    """
    Make a prediction using one of the trained models.
    
    Args:
        request: PredictionRequest containing model_name, model_type, and features
        
    Returns:
        PredictionResponse with prediction and confidence
        
    Example:
        POST /api/v1/prediction/predict
        {
            "model_name": "RandomForest_v1",
            "model_type": "classification",
            "features": {
                "feature_1": 0.5,
                "feature_2": -0.2,
                "feature_3": 1.0,
                "feature_4": 50.0,
                "feature_5": 1
            }
        }
    """
    try:
        model_name = request.model_name
        model_type = request.model_type
        features = request.features
        
        logger.info(f"Processing prediction request: model={model_name}, type={model_type}")
        
        # Validate model type
        if model_type not in ["classification", "regression", "clustering"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model_type: {model_type}. Must be 'classification', 'regression', or 'clustering'"
            )
        
        # Convert features to DataFrame for sklearn models
        features_df = pd.DataFrame([features])
        
        if model_type == "classification":
            return await _predict_classification(model_name, features_df)
        elif model_type == "regression":
            return await _predict_regression(model_name, features_df)
        elif model_type == "clustering":
            return await _predict_clustering(model_name, features_df)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


async def _predict_classification(model_name: str, features: pd.DataFrame) -> Dict[str, Any]:
    """Make classification prediction."""
    try:
        # Get classification results
        cls_results = loader.get("cls_results")
        if not cls_results or model_name not in cls_results:
            raise HTTPException(
                status_code=404,
                detail=f"Classification model '{model_name}' not found"
            )
        
        # Get the actual model (if available in loader)
        # For now, we'll return the model info with a simulated prediction
        model_info = cls_results[model_name]
        
        # Simulate prediction (in production, you'd load and run the actual model)
        prediction = int(np.random.choice([0, 1]))
        confidence = float(np.random.uniform(0.5, 1.0))
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "model_name": model_name,
            "model_type": "classification",
            "model_info": {
                "accuracy": model_info.get("accuracy", 0),
                "f1": model_info.get("f1", 0)
            }
        }
    except Exception as e:
        logger.error(f"Classification prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def _predict_regression(model_name: str, features: pd.DataFrame) -> Dict[str, Any]:
    """Make regression prediction."""
    try:
        # Get regression results
        reg_results = loader.get("reg_results")
        if not reg_results or model_name not in reg_results:
            raise HTTPException(
                status_code=404,
                detail=f"Regression model '{model_name}' not found"
            )
        
        model_info = reg_results[model_name]
        
        # Simulate prediction
        prediction = float(np.random.uniform(0, 100))
        confidence = float(model_info.get("r2", 0.5))
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "model_name": model_name,
            "model_type": "regression",
            "model_info": {
                "rmse": model_info.get("rmse", 0),
                "r2": model_info.get("r2", 0)
            }
        }
    except Exception as e:
        logger.error(f"Regression prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def _predict_clustering(model_name: str, features: pd.DataFrame) -> Dict[str, Any]:
    """Assign point to cluster."""
    try:
        kmeans = loader.get("kmeans")
        if not kmeans:
            raise HTTPException(
                status_code=404,
                detail="Clustering model not found"
            )
        
        # Simulate clustering prediction
        cluster = int(np.random.choice([0, 1, 2]))
        
        return {
            "prediction": cluster,
            "confidence": None,
            "model_name": "KMeans_v1",
            "model_type": "clustering",
            "model_info": {
                "n_clusters": 3,
                "inertia": 0
            }
        }
    except Exception as e:
        logger.error(f"Clustering prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predict/available-models")
async def get_available_models() -> Dict[str, Any]:
    """Get all available models for prediction."""
    try:
        models_info = {
            "classification": [],
            "regression": [],
            "clustering": [],
            "forecasting": []
        }
        
        # Get classification models
        cls_results = loader.get("cls_results")
        if cls_results:
            models_info["classification"] = list(cls_results.keys())
        
        # Get regression models
        reg_results = loader.get("reg_results")
        if reg_results:
            models_info["regression"] = list(reg_results.keys())
        
        # Get clustering model
        kmeans = loader.get("kmeans")
        if kmeans:
            models_info["clustering"] = ["KMeans_v1"]
        
        # Get forecasting model
        ts_results = loader.get("ts_results")
        if ts_results:
            models_info["forecasting"] = ["ARIMA_v1", "RandomForest_v1"]
        
        return models_info
    except Exception as e:
        logger.error(f"Error fetching available models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-predict")
async def batch_predict(requests: List[PredictionRequest]) -> List[Dict[str, Any]]:
    """
    Make predictions for multiple inputs at once.
    
    Args:
        requests: List of PredictionRequest objects
        
    Returns:
        List of predictions
    """
    try:
        results = []
        for request in requests:
            result = await predict(request)
            results.append(result)
        return results
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
