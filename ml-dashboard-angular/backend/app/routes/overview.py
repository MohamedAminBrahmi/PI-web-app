"""Overview and dataset statistics endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.models_loader import ModelsLoader

router = APIRouter(prefix="/overview", tags=["Overview"])
loader = ModelsLoader()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    try:
        if not loader.is_loaded():
            raise HTTPException(status_code=503, detail="Models not loaded")
        return {"status": "healthy", "models_loaded": str(len(loader.models))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_dataset_stats() -> Dict[str, Any]:
    """Get dataset statistics."""
    try:
        master = loader.get("master")
        cls_results = loader.get("cls_results")
        reg_results = loader.get("reg_results")
        ts_data = loader.get("ts_data")
        
        if master is None:
            raise HTTPException(status_code=404, detail="Master data not found")
        
        stats = {
            "total_records": len(master),
            "total_columns": len(master.columns),
            "date_range": {
                "start": master.get("event_date", master.get("date")).min().isoformat() if "event_date" in master.columns or "date" in master.columns else None,
                "end": master.get("event_date", master.get("date")).max().isoformat() if "event_date" in master.columns or "date" in master.columns else None,
            },
            "missing_values": master.isnull().sum().to_dict(),
            "numeric_summary": master.describe().to_dict(),
            "models": {
                "classification": list(cls_results.keys()) if cls_results else [],
                "regression": list(reg_results.keys()) if reg_results else [],
                "time_series": list(ts_data.keys()) if ts_data else [],
            }
        }
        
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models-info")
async def get_models_info() -> Dict[str, Any]:
    """Get information about all trained models."""
    try:
        cls_results = loader.get("cls_results")
        reg_results = loader.get("reg_results")
        
        info = {
            "classification": {},
            "regression": {}
        }
        
        if cls_results:
            for model_name, results in cls_results.items():
                info["classification"][model_name] = {
                    "accuracy": float(results.get("accuracy", 0)),
                    "precision": float(results.get("precision", 0)),
                    "recall": float(results.get("recall", 0)),
                    "f1": float(results.get("f1", 0)),
                    "auc": float(results.get("auc", 0)),
                }
        
        if reg_results:
            for model_name, results in reg_results.items():
                info["regression"][model_name] = {
                    "mse": float(results.get("mse", 0)),
                    "rmse": float(results.get("rmse", 0)),
                    "mae": float(results.get("mae", 0)),
                    "r2": float(results.get("r2", 0)),
                }
        
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
