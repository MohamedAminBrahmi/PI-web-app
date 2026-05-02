"""Prometheus metrics for ML Dashboard API."""
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
from typing import Dict
import time

# Create a custom registry
registry = CollectorRegistry()

# API Metrics
request_count = Counter(
    'ml_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

request_duration = Histogram(
    'ml_api_request_duration_seconds',
    'API request latency in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0),
    registry=registry
)

request_size = Histogram(
    'ml_api_request_size_bytes',
    'API request size in bytes',
    ['method', 'endpoint'],
    registry=registry
)

response_size = Histogram(
    'ml_api_response_size_bytes',
    'API response size in bytes',
    ['method', 'endpoint'],
    registry=registry
)

# Model Prediction Metrics
predictions_total = Counter(
    'ml_predictions_total',
    'Total predictions made',
    ['model_type', 'status'],
    registry=registry
)

prediction_latency = Histogram(
    'ml_prediction_latency_seconds',
    'Model prediction latency in seconds',
    ['model_type'],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5),
    registry=registry
)

prediction_confidence = Gauge(
    'ml_prediction_confidence',
    'Average prediction confidence score',
    ['model_type'],
    registry=registry
)

# Model Performance Metrics
model_accuracy = Gauge(
    'ml_model_accuracy',
    'Model accuracy',
    ['model_type'],
    registry=registry
)

model_precision = Gauge(
    'ml_model_precision',
    'Model precision',
    ['model_type'],
    registry=registry
)

model_recall = Gauge(
    'ml_model_recall',
    'Model recall',
    ['model_type'],
    registry=registry
)

# Data Quality Metrics
data_missing_values = Gauge(
    'ml_data_missing_values_percent',
    'Percentage of missing values in data',
    ['dataset'],
    registry=registry
)

data_freshness_hours = Gauge(
    'ml_data_freshness_hours',
    'Data freshness in hours',
    ['dataset'],
    registry=registry
)

# System Metrics
system_errors = Counter(
    'ml_system_errors_total',
    'Total system errors',
    ['error_type'],
    registry=registry
)

active_requests = Gauge(
    'ml_active_requests',
    'Number of active requests',
    registry=registry
)

# Drift Detection Metrics
data_drift_detected = Counter(
    'ml_data_drift_detected_total',
    'Number of data drift detections',
    ['feature'],
    registry=registry
)

model_drift_detected = Counter(
    'ml_model_drift_detected_total',
    'Number of model drift detections',
    ['model_type'],
    registry=registry
)

accuracy_drop_alert = Counter(
    'ml_accuracy_drop_alerts_total',
    'Number of accuracy drop alerts',
    ['model_type'],
    registry=registry
)

confidence_drop_alert = Counter(
    'ml_confidence_drop_alerts_total',
    'Number of confidence drop alerts',
    ['model_type'],
    registry=registry
)

# Baseline Comparison Metrics
accuracy_vs_baseline = Gauge(
    'ml_accuracy_vs_baseline_percent',
    'Accuracy deviation from baseline in percent',
    ['model_type'],
    registry=registry
)

latency_vs_baseline = Gauge(
    'ml_latency_vs_baseline_percent',
    'Latency deviation from baseline in percent',
    registry=registry
)

confidence_vs_baseline = Gauge(
    'ml_confidence_vs_baseline_percent',
    'Confidence deviation from baseline in percent',
    registry=registry
)


class MetricsCollector:
    """Centralized metrics collection."""
    
    def __init__(self):
        self.baseline_metrics = {
            'accuracy': 0.85,
            'latency': 0.05,  # seconds
            'confidence': 0.75
        }
        self.request_count = 0
        self.error_count = 0
        self.predictions_cache = []
        
    def record_request(self, method: str, endpoint: str, status: int, duration: float, request_size_bytes: int, response_size_bytes: int):
        """Record API request metrics."""
        request_count.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
        request_size.labels(method=method, endpoint=endpoint).observe(request_size_bytes)
        response_size.labels(method=method, endpoint=endpoint).observe(response_size_bytes)
        self.request_count += 1
        
    def record_prediction(self, model_type: str, latency: float, confidence: float, status: str = "success"):
        """Record prediction metrics."""
        predictions_total.labels(model_type=model_type, status=status).inc()
        prediction_latency.labels(model_type=model_type).observe(latency)
        prediction_confidence.labels(model_type=model_type).set(confidence)
        self.predictions_cache.append({
            'model_type': model_type,
            'latency': latency,
            'confidence': confidence,
            'timestamp': time.time()
        })
        
    def record_error(self, error_type: str):
        """Record system errors."""
        system_errors.labels(error_type=error_type).inc()
        self.error_count += 1
        
    def update_model_performance(self, model_type: str, accuracy: float, precision: float, recall: float):
        """Update model performance metrics."""
        model_accuracy.labels(model_type=model_type).set(accuracy)
        model_precision.labels(model_type=model_type).set(precision)
        model_recall.labels(model_type=model_type).set(recall)
        
        # Calculate deviation from baseline
        baseline_acc = self.baseline_metrics['accuracy']
        acc_deviation = ((accuracy - baseline_acc) / baseline_acc) * 100
        accuracy_vs_baseline.labels(model_type=model_type).set(acc_deviation)
        
    def set_active_requests(self, count: int):
        """Set number of active requests."""
        active_requests.set(count)
        
    def check_accuracy_degradation(self, model_type: str, current_accuracy: float):
        """Check if accuracy dropped more than 5%."""
        threshold = self.baseline_metrics['accuracy'] * 0.95  # 5% drop
        if current_accuracy < threshold:
            accuracy_drop_alert.labels(model_type=model_type).inc()
            return True
        return False
    
    def check_confidence_degradation(self, model_type: str, current_confidence: float):
        """Check if confidence dropped."""
        threshold = self.baseline_metrics['confidence'] * 0.95
        if current_confidence < threshold:
            confidence_drop_alert.labels(model_type=model_type).inc()
            return True
        return False
    
    def detect_data_drift(self, feature: str, drift_detected: bool):
        """Record data drift detection."""
        if drift_detected:
            data_drift_detected.labels(feature=feature).inc()
            return True
        return False
    
    def detect_model_drift(self, model_type: str, drift_score: float):
        """Record model drift detection."""
        # If drift score > 0.3 (30%), mark as drift
        if drift_score > 0.3:
            model_drift_detected.labels(model_type=model_type).inc()
            return True
        return False
    
    def get_error_rate(self) -> float:
        """Calculate current error rate."""
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100


# Global metrics collector instance
metrics_collector = MetricsCollector()
