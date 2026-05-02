"""Clustering model endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import numpy as np
from app.models_loader import ModelsLoader

router = APIRouter(prefix="/clustering", tags=["Clustering"])
loader = ModelsLoader()


@router.get("/pca-visualization")
async def get_pca_visualization() -> Dict[str, Any]:
    """Get PCA coordinates for 2D visualization."""
    try:
        pca_coords = loader.get("pca_coords")
        cluster_df = loader.get("cluster_df")
        
        if pca_coords is None or cluster_df is None:
            raise HTTPException(status_code=404, detail="Clustering data not found")
        
        # Extract PCA components
        pca_x = pca_coords[:, 0].tolist() if pca_coords.ndim > 1 else [pca_coords]
        pca_y = pca_coords[:, 1].tolist() if pca_coords.ndim > 1 else [pca_coords]
        
        # Get cluster labels
        kmeans_clusters = cluster_df["kmeans_cluster"].tolist() if "kmeans_cluster" in cluster_df.columns else []
        
        return {
            "pca": {
                "x": pca_x,
                "y": pca_y,
            },
            "clusters": kmeans_clusters,
            "features": [
                col for col in cluster_df.columns
                if col not in ["kmeans_cluster", "agglo_cluster"]
            ][:10],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/silhouette-analysis")
async def get_silhouette_analysis() -> Dict[str, Any]:
    """Get silhouette scores for different k values."""
    try:
        sil_by_k = loader.get("sil_by_k")
        
        if not sil_by_k:
            raise HTTPException(status_code=404, detail="Silhouette data not found")
        
        # Convert numpy values to Python floats
        silhouette_data = {
            str(k): float(v) for k, v in sil_by_k.items()
        }
        
        best_k = max(sil_by_k, key=sil_by_k.get)
        
        return {
            "silhouette_scores": silhouette_data,
            "best_k": int(best_k),
            "best_score": float(sil_by_k[best_k]),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clusters-summary")
async def get_clusters_summary() -> Dict[str, Any]:
    """Get summary statistics for each cluster."""
    try:
        cluster_df = loader.get("cluster_df")
        
        if cluster_df is None:
            raise HTTPException(status_code=404, detail="Cluster data not found")
        
        # Group by kmeans clusters
        summary = {}
        if "kmeans_cluster" in cluster_df.columns:
            for cluster_id in cluster_df["kmeans_cluster"].unique():
                cluster_data = cluster_df[cluster_df["kmeans_cluster"] == cluster_id]
                summary[f"cluster_{int(cluster_id)}"] = {
                    "size": len(cluster_data),
                    "units": cluster_data.get("unit_name", []).tolist()[:5],
                    "avg_events": float(cluster_data["nb_events"].mean()),
                    "avg_participants": float(cluster_data["total_participants"].mean()),
                }
        
        return {"clusters": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
