"""FastAPI main application."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import logging
from pathlib import Path
import time

from app.config import API_V1_STR, PROJECT_NAME, PROJECT_VERSION, ALLOWED_ORIGINS, MODELS_DIR
from app.models_loader import ModelsLoader
from app.routes import overview, classification, regression, clustering, forecasting, prediction
from app.monitoring import metrics_collector, registry, DriftDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize drift detector
drift_detector = DriftDetector(window_size=100, sensitivity=0.3)

# Initialize FastAPI
app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description="REST API for ML Dashboard - serving classification, regression, clustering, and forecasting models with monitoring"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Prometheus Metrics Middleware
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    """Middleware to track request metrics."""
    start_time = time.time()
    request_size = 0
    
    # Try to get request size
    if request.headers.get('content-length'):
        request_size = int(request.headers['content-length'])
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    response_size = response.headers.get('content-length', 0)
    
    # Record metrics
    metrics_collector.record_request(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
        duration=duration,
        request_size_bytes=request_size,
        response_size_bytes=int(response_size) if response_size else 0
    )
    
    # Add latency to response headers
    response.headers["X-Process-Time"] = str(duration)
    
    return response


# Load models on startup
@app.on_event("startup")
async def startup_event():
    """Load all models when app starts."""
    logger.info("Loading ML models...")
    try:
        loader = ModelsLoader()
        loader.load_models(MODELS_DIR)
        logger.info(f"✓ Loaded {len(loader.models)} model artifacts")
        
        # Initialize baseline metrics
        metrics_collector.baseline_metrics = {
            'accuracy': 0.85,
            'latency': 0.05,
            'confidence': 0.75
        }
        logger.info(f"✓ Baseline metrics initialized: {metrics_collector.baseline_metrics}")
        
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise


# Include routers
app.include_router(overview.router, prefix=API_V1_STR)
app.include_router(classification.router, prefix=API_V1_STR)
app.include_router(regression.router, prefix=API_V1_STR)
app.include_router(clustering.router, prefix=API_V1_STR)
app.include_router(forecasting.router, prefix=API_V1_STR)
app.include_router(prediction.router, prefix=API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ML Dashboard API",
        "version": PROJECT_VERSION,
        "docs": "/docs",
        "api": f"{API_V1_STR}/",
        "metrics": "/metrics",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ML Dashboard API",
        "version": PROJECT_VERSION,
        "error_rate": f"{metrics_collector.get_error_rate():.2f}%",
        "total_requests": metrics_collector.request_count,
        "total_errors": metrics_collector.error_count
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/api/v1/monitoring/drift-summary")
async def drift_summary():
    """Get drift detection summary."""
    feature_drifts = drift_detector.get_feature_drift_summary()
    pred_drift, pred_score = drift_detector.detect_prediction_drift()
    multi_drift, multi_score = drift_detector.detect_multivariate_drift()
    
    return {
        "feature_drifts": feature_drifts,
        "prediction_drift": {
            "detected": pred_drift,
            "score": float(pred_score)
        },
        "multivariate_drift": {
            "detected": multi_drift,
            "score": float(multi_score)
        }
    }


@app.get("/api/v1/monitoring/baseline")
async def get_baseline():
    """Get baseline metrics."""
    return {
        "baseline_metrics": metrics_collector.baseline_metrics,
        "request_count": metrics_collector.request_count,
        "error_count": metrics_collector.error_count,
        "error_rate": f"{metrics_collector.get_error_rate():.2f}%"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
