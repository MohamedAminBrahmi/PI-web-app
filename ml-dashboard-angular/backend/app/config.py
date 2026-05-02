"""Configuration settings for FastAPI backend."""
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# API Settings
API_V1_STR = "/api/v1"
PROJECT_NAME = "ML Dashboard API"
PROJECT_VERSION = "1.0.0"

# CORS Settings
ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:3000",
    "http://127.0.0.1:4200",
    "http://127.0.0.1:3000",
]

# Model paths
MODEL_PATHS = {
    "cls_results": MODELS_DIR / "cls_results.pkl",
    "label_encoder": MODELS_DIR / "label_encoder.pkl",
    "reg_results": MODELS_DIR / "reg_results.pkl",
    "cluster_df": MODELS_DIR / "cluster_df.pkl",
    "kmeans": MODELS_DIR / "kmeans.pkl",
    "pca_coords": MODELS_DIR / "pca_coords.pkl",
    "cluster_features": MODELS_DIR / "cluster_features.pkl",
    "sil_by_k": MODELS_DIR / "sil_by_k.pkl",
    "feature_cols": MODELS_DIR / "feature_cols.pkl",
    "cat_features": MODELS_DIR / "cat_features.pkl",
    "num_features": MODELS_DIR / "num_features.pkl",
    "ts_results": MODELS_DIR / "ts_results.pkl",
    "ts_data": MODELS_DIR / "ts_data.pkl",
    "master": MODELS_DIR / "master.pkl",
    "cluster_scaler": MODELS_DIR / "cluster_scaler.pkl",
}
