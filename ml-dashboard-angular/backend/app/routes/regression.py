"""Regression model endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import numpy as np
from app.models_loader import ModelsLoader

router = APIRouter(prefix="/regression", tags=["Regression"])
loader = ModelsLoader()


@router.get("/models")
async def get_regression_models() -> Dict[str, Any]:
    """List available regression models."""
    try:
        reg_results = loader.get("reg_results")
        if not reg_results:
            raise HTTPException(status_code=404, detail="No regression models found")
        
        models_list = {
            name: {
                "mse": float(results.get("mse", 0)),
                "rmse": float(results.get("rmse", 0)),
                "mae": float(results.get("mae", 0)),
                "r2": float(results.get("r2", 0)),
            }
            for name, results in reg_results.items()
        }
        
        return {"models": models_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/actual-vs-predicted/{model_name}")
async def get_actual_vs_predicted(model_name: str) -> Dict[str, Any]:
    """Get actual vs predicted values for regression model."""
    try:
        reg_results = loader.get("reg_results")
        if not reg_results or model_name not in reg_results:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        model_data = reg_results[model_name]
        y_test = model_data.get("y_test")
        pred = model_data.get("pred")
        
        if y_test is None or pred is None:
            raise HTTPException(status_code=400, detail="Missing prediction data")
        
        # Convert to lists for JSON serialization
        y_test_list = y_test.tolist() if hasattr(y_test, 'tolist') else list(y_test)
        pred_list = pred.tolist() if hasattr(pred, 'tolist') else list(pred)
        
        return {
            "model": model_name,
            "actual": y_test_list,
            "predicted": pred_list,
            "count": len(y_test_list),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/residuals/{model_name}")
async def get_residuals(model_name: str) -> Dict[str, Any]:
    """Get residuals for regression model."""
    try:
        reg_results = loader.get("reg_results")
        if not reg_results or model_name not in reg_results:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        model_data = reg_results[model_name]
        y_test = model_data.get("y_test")
        pred = model_data.get("pred")
        
        if y_test is None or pred is None:
            raise HTTPException(status_code=400, detail="Missing prediction data")
        
        residuals = (np.array(y_test) - np.array(pred)).tolist()
        
        return {
            "model": model_name,
            "residuals": residuals,
            "mean": float(np.mean(residuals)),
            "std": float(np.std(residuals)),
            "count": len(residuals),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{model_name}")
async def get_metrics(model_name: str) -> Dict[str, Any]:
    """Get all metrics for a regression model."""
    try:
        reg_results = loader.get("reg_results")
        if not reg_results or model_name not in reg_results:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        metrics = reg_results[model_name]
        
        return {
            "model": model_name,
            "mse": float(metrics.get("mse", 0)),
            "rmse": float(metrics.get("rmse", 0)),
            "mae": float(metrics.get("mae", 0)),
            "r2": float(metrics.get("r2", 0)),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
