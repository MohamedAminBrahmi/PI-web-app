"""Classification model endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import numpy as np
from app.models_loader import ModelsLoader

router = APIRouter(prefix="/classification", tags=["Classification"])
loader = ModelsLoader()


class ClassificationRequest(BaseModel):
    """Request model for classification prediction."""
    model_name: str
    features: Dict[str, Any]


@router.get("/models")
async def get_classification_models() -> Dict[str, Any]:
    """List available classification models."""
    try:
        cls_results = loader.get("cls_results")
        if not cls_results:
            raise HTTPException(status_code=404, detail="No classification models found")
        
        models_list = {
            name: {
                "accuracy": float(results.get("accuracy", 0)),
                "precision": float(results.get("precision", 0)),
                "recall": float(results.get("recall", 0)),
                "f1": float(results.get("f1", 0)),
                "auc": float(results.get("auc", 0)),
            }
            for name, results in cls_results.items()
        }
        
        return {"models": models_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/confusion-matrix/{model_name}")
async def get_confusion_matrix(model_name: str) -> Dict[str, Any]:
    """Get confusion matrix for a classification model."""
    try:
        cls_results = loader.get("cls_results")
        if not cls_results or model_name not in cls_results:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        from sklearn.metrics import confusion_matrix
        
        model_data = cls_results[model_name]
        y_test = model_data.get("y_test")
        pred = model_data.get("pred")
        
        if y_test is None or pred is None:
            raise HTTPException(status_code=400, detail="Missing test data")
        
        cm = confusion_matrix(y_test, pred)
        
        return {
            "model": model_name,
            "confusion_matrix": cm.tolist(),
            "shape": cm.shape,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roc-curve/{model_name}")
async def get_roc_curve(model_name: str) -> Dict[str, Any]:
    """Get ROC curve data for a classification model."""
    try:
        from sklearn.metrics import roc_curve, auc
        from sklearn.preprocessing import label_binarize
        
        cls_results = loader.get("cls_results")
        if not cls_results or model_name not in cls_results:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        model_data = cls_results[model_name]
        y_test = model_data.get("y_test")
        proba = model_data.get("proba")
        
        if y_test is None or proba is None:
            raise HTTPException(status_code=400, detail="Missing probability data")
        
        # Convert to binary classification for ROC
        y_bin = label_binarize(y_test, classes=np.unique(y_test))
        fpr, tpr, thresholds = roc_curve(y_bin.ravel(), proba.ravel())
        roc_auc = auc(fpr, tpr)
        
        return {
            "model": model_name,
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist(),
            "auc": float(roc_auc),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classification-report/{model_name}")
async def get_classification_report(model_name: str) -> Dict[str, Any]:
    """Get detailed classification report."""
    try:
        from sklearn.metrics import classification_report
        
        cls_results = loader.get("cls_results")
        if not cls_results or model_name not in cls_results:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        
        model_data = cls_results[model_name]
        y_test = model_data.get("y_test")
        pred = model_data.get("pred")
        
        if y_test is None or pred is None:
            raise HTTPException(status_code=400, detail="Missing test data")
        
        report = classification_report(y_test, pred, output_dict=True)
        
        return {"model": model_name, "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
