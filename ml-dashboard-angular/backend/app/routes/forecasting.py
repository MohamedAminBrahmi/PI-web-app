"""Time series forecasting endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import numpy as np
from app.models_loader import ModelsLoader

router = APIRouter(prefix="/forecasting", tags=["Forecasting"])
loader = ModelsLoader()


@router.get("/models")
async def get_forecasting_models() -> Dict[str, Any]:
    """List available time series models."""
    try:
        ts_results = loader.get("ts_results")
        
        if not ts_results:
            raise HTTPException(status_code=404, detail="No time series models found")
        
        models_list = {
            name: {
                "rmse": float(results.get("rmse", 0)),
                "mae": float(results.get("mae", 0)),
                "mape": float(results.get("mape", 0)),
            }
            for name, results in ts_results.items()
        }
        
        return {"models": models_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast/{model_name}")
async def get_forecast(model_name: str) -> Dict[str, Any]:
    """Get forecast predictions for a time series model."""
    try:
        ts_results = loader.get("ts_results")
        ts_data = loader.get("ts_data")
        
        if not ts_results or model_name not in ts_results:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        model_data = ts_results[model_name]
        test_data = ts_data.get("test") if ts_data else None
        
        if test_data is None:
            raise HTTPException(status_code=400, detail="Missing test data")
        
        pred = model_data.get("pred")
        if pred is None:
            raise HTTPException(status_code=400, detail="Missing predictions")
        
        # Convert to lists
        pred_list = pred.tolist() if hasattr(pred, 'tolist') else list(pred)
        test_list = test_data.tolist() if hasattr(test_data, 'tolist') else list(test_data)
        
        return {
            "model": model_name,
            "actual": test_list,
            "predicted": pred_list,
            "rmse": float(model_data.get("rmse", 0)),
            "mae": float(model_data.get("mae", 0)),
            "mape": float(model_data.get("mape", 0)),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/time-series-data")
async def get_time_series_data() -> Dict[str, Any]:
    """Get time series training and test data."""
    try:
        ts_data = loader.get("ts_data")
        
        if not ts_data:
            raise HTTPException(status_code=404, detail="Time series data not found")
        
        train = ts_data.get("train")
        test = ts_data.get("test")
        
        train_list = train.tolist() if hasattr(train, 'tolist') else list(train)
        test_list = test.tolist() if hasattr(test, 'tolist') else list(test)
        
        return {
            "train": train_list,
            "test": test_list,
            "train_size": len(train_list),
            "test_size": len(test_list),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
