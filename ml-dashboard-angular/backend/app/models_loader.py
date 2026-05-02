"""Load and manage ML models from pickle files."""
import joblib
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import pickle
import sys

logger = logging.getLogger(__name__)

# Register unpickler to handle missing pyarrow gracefully
class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'pyarrow' and name.startswith('_lib'):
            # Try to import from the correct location
            try:
                import pyarrow._lib
                return getattr(pyarrow._lib, name)
            except (ImportError, AttributeError):
                logger.warning(f"Could not import {module}.{name}, continuing anyway")
                # Return a dummy class to prevent crash
                return object
        return super().find_class(module, name)


class ModelsLoader:
    """Singleton class to load and cache all ML models."""
    
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_models(self, models_dir: Path) -> Dict[str, Any]:
        """Load all pickle files from models directory."""
        if self._models:
            return self._models
        
        try:
            # Import pyarrow before loading models to ensure it's available
            try:
                import pyarrow
                logger.info("✓ PyArrow available")
            except ImportError:
                logger.warning("PyArrow not available, some models may fail to load")
            
            model_files = {
                "cls_results": "cls_results.pkl",
                "label_encoder": "label_encoder.pkl",
                "reg_results": "reg_results.pkl",
                "cluster_df": "cluster_df.pkl",
                "kmeans": "kmeans.pkl",
                "pca_coords": "pca_coords.pkl",
                "cluster_features": "cluster_features.pkl",
                "sil_by_k": "sil_by_k.pkl",
                "feature_cols": "feature_cols.pkl",
                "cat_features": "cat_features.pkl",
                "num_features": "num_features.pkl",
                "ts_results": "ts_results.pkl",
                "ts_data": "ts_data.pkl",
                "master": "master.pkl",
                "cluster_scaler": "cluster_scaler.pkl",
            }
            
            # Ensure models_dir exists
            if not models_dir.exists():
                logger.warning(f"Models directory does not exist: {models_dir}")
                return self._models
            
            for key, filename in model_files.items():
                file_path = models_dir / filename
                if file_path.exists():
                    try:
                        self._models[key] = joblib.load(file_path)
                        logger.info(f"✓ Loaded {key} from {file_path}")
                    except Exception as e:
                        logger.error(f"✗ Failed to load {key}: {str(e)}")
                        # Continue loading other models even if one fails
                else:
                    logger.warning(f"✗ Missing {filename} at {file_path}")
            
            if not self._models:
                logger.warning("No models were loaded successfully")
            else:
                logger.info(f"✓ Successfully loaded {len(self._models)} model artifacts")
            
            return self._models
        
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            # Don't re-raise, return empty dict so the app can still start
            return self._models
    
    @property
    def models(self) -> Dict[str, Any]:
        """Get loaded models."""
        return self._models
    
    def get(self, key: str) -> Optional[Any]:
        """Get a specific model by key."""
        return self._models.get(key)
    
    def is_loaded(self) -> bool:
        """Check if models are loaded."""
        return len(self._models) > 0
