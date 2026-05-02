"""
Automated ML Training Pipeline with MLflow Tracking
Handles: Preprocessing → Training → Evaluation → Model Saving & Versioning
"""

import os
import sys
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple, List
import pickle
import warnings

import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score, silhouette_score,
    confusion_matrix, classification_report, roc_curve, auc
)
from sklearn.linear_model import LinearRegression
import joblib

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
MLFLOW_DIR = PROJECT_ROOT / "mlruns"

# Create directories if they don't exist
MODELS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
MLFLOW_DIR.mkdir(exist_ok=True)

# Set MLflow tracking URI
mlflow.set_tracking_uri(f"file:{MLFLOW_DIR}")
mlflow.set_experiment("ML_Dashboard_Training")


class DataGenerator:
    """Generate synthetic datasets for demonstration."""
    
    @staticmethod
    def generate_synthetic_data(n_samples: int = 1000) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Generate synthetic datasets for all model types."""
        logger.info(f"Generating synthetic data with {n_samples} samples...")
        
        np.random.seed(42)
        
        # Create feature matrix
        X = pd.DataFrame({
            'feature_1': np.random.randn(n_samples),
            'feature_2': np.random.randn(n_samples),
            'feature_3': np.random.randn(n_samples) * 2 + 1,
            'feature_4': np.random.uniform(0, 100, n_samples),
            'feature_5': np.random.choice([0, 1, 2], n_samples),
        })
        
        # Create target for classification
        y_classification = (X['feature_1'] + X['feature_2'] > 0).astype(int)
        
        # Create target for regression
        y_regression = 2 * X['feature_1'] + 3 * X['feature_2'] + np.random.randn(n_samples) * 0.5
        
        # Create target for time series
        time_series = np.cumsum(np.random.randn(200)) + 100
        
        return X, pd.DataFrame({
            'classification': y_classification,
            'regression': y_regression,
            'time_series': time_series[:n_samples]
        })
    
    @staticmethod
    def load_or_generate_data(data_path: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load data from file or generate synthetic data."""
        if data_path.exists():
            logger.info(f"Loading data from {data_path}")
            X = pd.read_csv(data_path / "X.csv", index_col=0)
            y = pd.read_csv(data_path / "y.csv", index_col=0)
            return X, y
        else:
            logger.warning(f"Data not found at {data_path}. Generating synthetic data...")
            X, y = DataGenerator.generate_synthetic_data()
            data_path.mkdir(exist_ok=True)
            X.to_csv(data_path / "X.csv")
            y.to_csv(data_path / "y.csv")
            return X, y


class ClassificationPipeline:
    """Training pipeline for classification models."""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
    
    def train(self, X: pd.DataFrame, y: pd.Series, run_name: str = "classification_training"):
        """Train classification models with MLflow tracking."""
        logger.info("Starting Classification Training Pipeline...")
        
        with mlflow.start_run(run_name=run_name):
            # Preprocessing
            X_processed = self._preprocess(X)
            X_train, X_test, y_train, y_test = train_test_split(
                X_processed, y, test_size=0.2, random_state=42
            )
            
            # Train multiple classification models
            model_configs = {
                'RandomForest_v1': RandomForestClassifier(n_estimators=100, random_state=42),
                'RandomForest_v2': RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
            }
            
            for model_name, model in model_configs.items():
                logger.info(f"Training {model_name}...")
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1]
                
                # Calculate metrics
                metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, zero_division=0),
                    'recall': recall_score(y_test, y_pred, zero_division=0),
                    'f1': f1_score(y_test, y_pred, zero_division=0),
                    'auc': roc_auc_score(y_test, y_pred_proba),
                    'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                    'classification_report': classification_report(y_test, y_pred, output_dict=True),
                    'roc_curve': {
                        'fpr': roc_curve(y_test, y_pred_proba)[0].tolist(),
                        'tpr': roc_curve(y_test, y_pred_proba)[1].tolist(),
                    }
                }
                
                # Log metrics to MLflow
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        mlflow.log_metric(f"{model_name}/{metric_name}", metric_value)
                
                mlflow.log_param(f"{model_name}/n_estimators", model.n_estimators)
                
                self.models[model_name] = model
                self.results[model_name] = metrics
                
                logger.info(f"✓ {model_name} - Accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1']:.4f}")
            
            # Log artifacts
            mlflow.log_dict(self.results, "classification_results.json")
            
        return self.models, self.results
    
    def _preprocess(self, X: pd.DataFrame) -> pd.DataFrame:
        """Preprocess features."""
        X_copy = X.copy()
        
        # Fit scaler on training data
        X_scaled = self.scaler.fit_transform(X_copy)
        
        return pd.DataFrame(X_scaled, columns=X_copy.columns)
    
    def save_models(self, save_dir: Path):
        """Save classification models and artifacts."""
        save_dir.mkdir(exist_ok=True)
        
        joblib.dump(self.results, save_dir / "cls_results.pkl")
        joblib.dump(self.scaler, save_dir / "classifier_scaler.pkl")
        
        logger.info(f"✓ Saved classification results to {save_dir / 'cls_results.pkl'}")


class RegressionPipeline:
    """Training pipeline for regression models."""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
    
    def train(self, X: pd.DataFrame, y: pd.Series, run_name: str = "regression_training"):
        """Train regression models with MLflow tracking."""
        logger.info("Starting Regression Training Pipeline...")
        
        with mlflow.start_run(run_name=run_name):
            # Preprocessing
            X_processed = self._preprocess(X)
            X_train, X_test, y_train, y_test = train_test_split(
                X_processed, y, test_size=0.2, random_state=42
            )
            
            # Train multiple regression models
            model_configs = {
                'LinearRegression': LinearRegression(),
                'RandomForest_v1': RandomForestRegressor(n_estimators=100, random_state=42),
                'RandomForest_v2': RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
            }
            
            for model_name, model in model_configs.items():
                logger.info(f"Training {model_name}...")
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                residuals = y_test - y_pred
                metrics = {
                    'mse': mean_squared_error(y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'mae': mean_absolute_error(y_test, y_pred),
                    'r2': r2_score(y_test, y_pred),
                    'actual_vs_predicted': {
                        'actual': y_test.tolist(),
                        'predicted': y_pred.tolist(),
                    },
                    'residuals': residuals.tolist(),
                }
                
                # Log metrics to MLflow
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        mlflow.log_metric(f"{model_name}/{metric_name}", metric_value)
                
                self.models[model_name] = model
                self.results[model_name] = metrics
                
                logger.info(f"✓ {model_name} - RMSE: {metrics['rmse']:.4f}, R²: {metrics['r2']:.4f}")
            
            # Log artifacts
            mlflow.log_dict(self.results, "regression_results.json")
        
        return self.models, self.results
    
    def _preprocess(self, X: pd.DataFrame) -> pd.DataFrame:
        """Preprocess features."""
        X_copy = X.copy()
        X_scaled = self.scaler.fit_transform(X_copy)
        return pd.DataFrame(X_scaled, columns=X_copy.columns)
    
    def save_models(self, save_dir: Path):
        """Save regression models and artifacts."""
        save_dir.mkdir(exist_ok=True)
        
        joblib.dump(self.results, save_dir / "reg_results.pkl")
        joblib.dump(self.scaler, save_dir / "regression_scaler.pkl")
        
        logger.info(f"✓ Saved regression results to {save_dir / 'reg_results.pkl'}")


class ClusteringPipeline:
    """Training pipeline for clustering models."""
    
    def __init__(self):
        self.kmeans = None
        self.pca = None
        self.results = {}
        self.scaler = StandardScaler()
    
    def train(self, X: pd.DataFrame, run_name: str = "clustering_training"):
        """Train clustering models with MLflow tracking."""
        logger.info("Starting Clustering Training Pipeline...")
        
        with mlflow.start_run(run_name=run_name):
            # Preprocessing
            X_processed = self._preprocess(X)
            
            # PCA for visualization
            self.pca = PCA(n_components=2, random_state=42)
            X_pca = self.pca.fit_transform(X_processed)
            
            # KMeans clustering
            n_clusters = 3
            self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = self.kmeans.fit_predict(X_processed)
            
            # Calculate silhouette scores for different k values
            silhouette_scores = {}
            for k in range(2, 8):
                kmeans_k = KMeans(n_clusters=k, random_state=42, n_init=10)
                cluster_labels = kmeans_k.fit_predict(X_processed)
                score = silhouette_score(X_processed, cluster_labels)
                silhouette_scores[k] = score
                mlflow.log_metric(f"silhouette_score_k{k}", score)
                logger.info(f"K={k}, Silhouette Score: {score:.4f}")
            
            # Store results
            self.results = {
                'clusters': clusters.tolist(),
                'pca_coords': X_pca.tolist(),
                'silhouette_scores': silhouette_scores,
                'cluster_centers': self.kmeans.cluster_centers_.tolist(),
                'inertia': self.kmeans.inertia_,
            }
            
            mlflow.log_dict(self.results, "clustering_results.json")
            
            logger.info(f"✓ Clustering trained with {n_clusters} clusters")
        
        return self.results
    
    def _preprocess(self, X: pd.DataFrame) -> pd.DataFrame:
        """Preprocess features."""
        X_copy = X.copy()
        X_scaled = self.scaler.fit_transform(X_copy)
        return pd.DataFrame(X_scaled, columns=X_copy.columns)
    
    def save_models(self, save_dir: Path):
        """Save clustering models and artifacts."""
        save_dir.mkdir(exist_ok=True)
        
        joblib.dump(self.results, save_dir / "cluster_results.pkl")
        joblib.dump(self.kmeans, save_dir / "kmeans.pkl")
        joblib.dump(self.pca, save_dir / "pca.pkl")
        joblib.dump(self.scaler, save_dir / "cluster_scaler.pkl")
        
        logger.info(f"✓ Saved clustering results to {save_dir}")


class ForecastingPipeline:
    """Training pipeline for time series forecasting."""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
    
    def train(self, time_series: pd.Series, run_name: str = "forecasting_training"):
        """Train forecasting models with MLflow tracking."""
        logger.info("Starting Forecasting Training Pipeline...")
        
        with mlflow.start_run(run_name=run_name):
            # Prepare data
            data = time_series.values.reshape(-1, 1)
            X_scaled = self.scaler.fit_transform(data)
            
            # Create sliding window features
            window_size = 5
            X, y = self._create_sequences(X_scaled, window_size)
            
            if len(X) > 0:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                # Train forecasting model
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train, y_train.ravel())
                
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                metrics = {
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'mae': mean_absolute_error(y_test, y_pred),
                    'r2': r2_score(y_test, y_pred),
                }
                
                for metric_name, metric_value in metrics.items():
                    mlflow.log_metric(f"forecasting/{metric_name}", metric_value)
                
                self.results = {
                    'forecast': y_pred.tolist(),
                    'actual': y_test.tolist(),
                    'metrics': metrics,
                    'time_series_data': time_series.tolist()[:100],  # Store last 100 points
                }
                
                mlflow.log_dict(self.results, "forecasting_results.json")
                
                logger.info(f"✓ Forecasting trained - RMSE: {metrics['rmse']:.4f}")
        
        return self.results
    
    @staticmethod
    def _create_sequences(data: np.ndarray, window_size: int) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for time series."""
        X, y = [], []
        for i in range(len(data) - window_size):
            X.append(data[i:i + window_size])
            y.append(data[i + window_size])
        return np.array(X), np.array(y)
    
    def save_models(self, save_dir: Path):
        """Save forecasting models and artifacts."""
        save_dir.mkdir(exist_ok=True)
        
        joblib.dump(self.results, save_dir / "ts_results.pkl")
        joblib.dump(self.scaler, save_dir / "ts_scaler.pkl")
        
        logger.info(f"✓ Saved forecasting results to {save_dir / 'ts_results.pkl'}")


class TrainingPipeline:
    """Main orchestrator for the complete training pipeline."""
    
    def __init__(self, data_dir: Path, models_dir: Path):
        self.data_dir = data_dir
        self.models_dir = models_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run(self):
        """Execute the complete training pipeline."""
        logger.info("=" * 80)
        logger.info("🚀 Starting Complete ML Training Pipeline")
        logger.info(f"📁 Data Directory: {self.data_dir}")
        logger.info(f"📁 Models Directory: {self.models_dir}")
        logger.info(f"⏰ Timestamp: {self.timestamp}")
        logger.info("=" * 80)
        
        try:
            # Load or generate data
            X, y_dict = DataGenerator.load_or_generate_data(self.data_dir)
            
            # Classification
            logger.info("\n" + "=" * 40)
            logger.info("📊 CLASSIFICATION TRAINING")
            logger.info("=" * 40)
            cls_pipeline = ClassificationPipeline()
            cls_pipeline.train(X, y_dict['classification'])
            cls_pipeline.save_models(self.models_dir)
            
            # Regression
            logger.info("\n" + "=" * 40)
            logger.info("📈 REGRESSION TRAINING")
            logger.info("=" * 40)
            reg_pipeline = RegressionPipeline()
            reg_pipeline.train(X, y_dict['regression'])
            reg_pipeline.save_models(self.models_dir)
            
            # Clustering
            logger.info("\n" + "=" * 40)
            logger.info("🎯 CLUSTERING TRAINING")
            logger.info("=" * 40)
            cluster_pipeline = ClusteringPipeline()
            cluster_pipeline.train(X)
            cluster_pipeline.save_models(self.models_dir)
            
            # Forecasting
            logger.info("\n" + "=" * 40)
            logger.info("📉 FORECASTING TRAINING")
            logger.info("=" * 40)
            forecast_pipeline = ForecastingPipeline()
            forecast_pipeline.train(y_dict['time_series'])
            forecast_pipeline.save_models(self.models_dir)
            
            logger.info("\n" + "=" * 80)
            logger.info("✅ TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info(f"📁 Models saved to: {self.models_dir}")
            logger.info(f"📊 MLflow tracking: {MLFLOW_DIR}")
            logger.info("=" * 80)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Training pipeline failed: {str(e)}", exc_info=True)
            return False


def main():
    """Main entry point."""
    pipeline = TrainingPipeline(DATA_DIR, MODELS_DIR)
    success = pipeline.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
