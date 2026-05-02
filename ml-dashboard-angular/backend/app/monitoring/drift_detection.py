"""Data and Model Drift Detection."""
import numpy as np
from typing import Dict, List, Tuple
from scipy import stats
from collections import deque

class DriftDetector:
    """Detects data distribution shift and model drift."""
    
    def __init__(self, window_size: int = 100, sensitivity: float = 0.3):
        self.window_size = window_size
        self.sensitivity = sensitivity  # Drift threshold (0-1)
        
        # Store recent predictions for drift calculation
        self.prediction_history = deque(maxlen=window_size)
        self.feature_history = {}  # Track feature distributions
        self.baseline_distributions = {}
        
    def add_prediction(self, prediction: float, confidence: float):
        """Add prediction to history."""
        self.prediction_history.append({
            'prediction': prediction,
            'confidence': confidence
        })
    
    def add_feature_values(self, features: Dict[str, float]):
        """Add feature values to history."""
        for feature_name, value in features.items():
            if feature_name not in self.feature_history:
                self.feature_history[feature_name] = deque(maxlen=self.window_size)
            self.feature_history[feature_name].append(value)
    
    def set_baseline(self, features: Dict[str, List[float]]):
        """Set baseline feature distributions."""
        self.baseline_distributions = {
            name: {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values)
            }
            for name, values in features.items()
        }
    
    def detect_univariate_drift(self, feature_name: str, method: str = 'ks') -> Tuple[bool, float]:
        """
        Detect univariate drift in a single feature.
        
        Args:
            feature_name: Name of the feature to check
            method: 'ks' for Kolmogorov-Smirnov or 'hellinger' for Hellinger distance
            
        Returns:
            (drift_detected, drift_score)
        """
        if feature_name not in self.feature_history or feature_name not in self.baseline_distributions:
            return False, 0.0
        
        current_values = list(self.feature_history[feature_name])
        baseline = self.baseline_distributions[feature_name]
        
        if len(current_values) < 10:
            return False, 0.0
        
        if method == 'ks':
            # Kolmogorov-Smirnov test
            baseline_dist = np.random.normal(
                baseline['mean'], 
                baseline['std'], 
                1000
            )
            statistic, p_value = stats.ks_2samp(current_values, baseline_dist)
            
            # Normalize KS statistic to [0, 1]
            drift_score = min(statistic, 1.0)
            
        else:  # hellinger
            # Simplified Hellinger distance
            drift_score = self._hellinger_distance(
                current_values,
                baseline['mean'],
                baseline['std']
            )
        
        drift_detected = drift_score > self.sensitivity
        return drift_detected, drift_score
    
    def detect_multivariate_drift(self, method: str = 'mahalanobis') -> Tuple[bool, float]:
        """
        Detect multivariate drift across all features.
        
        Returns:
            (drift_detected, drift_score)
        """
        if not self.baseline_distributions or not self.feature_history:
            return False, 0.0
        
        drift_scores = []
        
        for feature_name in self.baseline_distributions.keys():
            _, score = self.detect_univariate_drift(feature_name)
            drift_scores.append(score)
        
        if not drift_scores:
            return False, 0.0
        
        # Average drift score across features
        avg_drift = np.mean(drift_scores)
        drift_detected = avg_drift > self.sensitivity
        
        return drift_detected, avg_drift
    
    def detect_prediction_drift(self) -> Tuple[bool, float]:
        """Detect drift in model predictions (confidence drops, accuracy changes)."""
        if len(self.prediction_history) < 10:
            return False, 0.0
        
        predictions = [p['prediction'] for p in self.prediction_history]
        confidences = [p['confidence'] for p in self.prediction_history]
        
        # Calculate drift based on confidence degradation
        confidence_mean = np.mean(confidences)
        confidence_std = np.std(confidences)
        
        # If confidence is very low or highly variable, indicate drift
        if confidence_mean < 0.6 or confidence_std > 0.2:
            drift_score = max(1 - confidence_mean, confidence_std)
            return drift_score > self.sensitivity, drift_score
        
        return False, 0.0
    
    def _hellinger_distance(self, current_values: List[float], baseline_mean: float, baseline_std: float) -> float:
        """Calculate Hellinger distance between current and baseline distributions."""
        current_mean = np.mean(current_values)
        current_std = np.std(current_values)
        
        # Simplified Hellinger distance for Gaussians
        if baseline_std == 0 or current_std == 0:
            return 0.0
        
        mean_diff = (current_mean - baseline_mean) ** 2
        var_ratio = (baseline_std ** 2) / (current_std ** 2)
        
        distance = np.sqrt(
            1 - np.sqrt(var_ratio) * np.exp(-mean_diff / (4 * current_std ** 2))
        )
        
        return min(distance, 1.0)
    
    def get_feature_drift_summary(self) -> Dict[str, Tuple[bool, float]]:
        """Get drift status for all features."""
        summary = {}
        for feature_name in self.baseline_distributions.keys():
            drift_detected, score = self.detect_univariate_drift(feature_name)
            summary[feature_name] = (drift_detected, score)
        return summary
    
    def reset(self):
        """Reset drift detector."""
        self.prediction_history.clear()
        self.feature_history.clear()
