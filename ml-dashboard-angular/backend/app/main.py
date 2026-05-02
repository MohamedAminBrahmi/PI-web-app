"""FastAPI main application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

from app.config import API_V1_STR, PROJECT_NAME, PROJECT_VERSION, ALLOWED_ORIGINS, MODELS_DIR
from app.models_loader import ModelsLoader
from app.routes import overview, classification, regression, clustering, forecasting, prediction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description="REST API for ML Dashboard - serving classification, regression, clustering, and forecasting models"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models on startup
@app.on_event("startup")
async def startup_event():
    """Load all models when app starts."""
    logger.info("Loading ML models...")
    try:
        loader = ModelsLoader()
        loader.load_models(MODELS_DIR)
        logger.info(f"✓ Loaded {len(loader.models)} model artifacts")
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
        "api": f"{API_V1_STR}/"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
