"""
Configuration and utility functions for ML training pipeline
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / "backend"
MODELS_DIR = BACKEND_DIR / "models"
DATA_DIR = BACKEND_DIR / "data"
MLRUNS_DIR = BACKEND_DIR / "mlruns"

# Create necessary directories
for directory in [MODELS_DIR, DATA_DIR, MLRUNS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# MLflow Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", f"file:{MLRUNS_DIR}")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "ML_Dashboard_Training")
MLFLOW_RUN_NAME = os.getenv("MLFLOW_RUN_NAME", None)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"

# Training Configuration
TRAIN_TEST_SPLIT = float(os.getenv("TRAIN_TEST_SPLIT", "0.2"))
RANDOM_STATE = int(os.getenv("RANDOM_STATE", "42"))
N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", "100"))

# Dataset Configuration
DATASET_SIZE = int(os.getenv("DATASET_SIZE", "1000"))
N_FEATURES = int(os.getenv("N_FEATURES", "5"))
N_CLUSTERS = int(os.getenv("N_CLUSTERS", "3"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", None)

# Feature names
FEATURE_NAMES = [f"feature_{i+1}" for i in range(N_FEATURES)]

# Configuration dictionary for easy access
CONFIG = {
    "project_root": PROJECT_ROOT,
    "models_dir": MODELS_DIR,
    "data_dir": DATA_DIR,
    "mlruns_dir": MLRUNS_DIR,
    "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
    "mlflow_experiment_name": MLFLOW_EXPERIMENT_NAME,
    "train_test_split": TRAIN_TEST_SPLIT,
    "random_state": RANDOM_STATE,
    "n_estimators": N_ESTIMATORS,
    "dataset_size": DATASET_SIZE,
    "n_features": N_FEATURES,
    "n_clusters": N_CLUSTERS,
    "feature_names": FEATURE_NAMES,
}


def print_config():
    """Print current configuration."""
    print("\n" + "=" * 80)
    print("🔧 CONFIGURATION SUMMARY")
    print("=" * 80)
    for key, value in CONFIG.items():
        if key != "feature_names":
            print(f"  {key:30s}: {value}")
    print(f"  {'feature_names':30s}: {', '.join(FEATURE_NAMES)}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    print_config()
