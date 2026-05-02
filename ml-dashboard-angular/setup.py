#!/usr/bin/env python3
"""
ML Dashboard Setup and Training Script
Initializes the ML training pipeline and sets up MLflow tracking
"""

import sys
import argparse
import logging
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

from config_utils import print_config, MODELS_DIR, DATA_DIR, MLRUNS_DIR
from train import TrainingPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_environment():
    """Create necessary directories and environment."""
    logger.info("Setting up environment...")
    
    dirs = [MODELS_DIR, DATA_DIR, MLRUNS_DIR]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Created directory: {dir_path}")
    
    return True


def run_training():
    """Run the training pipeline."""
    logger.info("Starting training pipeline...")
    
    pipeline = TrainingPipeline(DATA_DIR, MODELS_DIR)
    success = pipeline.run()
    
    if success:
        logger.info("✅ Training completed successfully!")
        logger.info(f"📁 Models saved to: {MODELS_DIR}")
        logger.info(f"📊 MLflow tracking to: {MLRUNS_DIR}")
        return True
    else:
        logger.error("❌ Training failed!")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ML Dashboard Setup and Training Script"
    )
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="Only setup environment without training"
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Show configuration and exit"
    )
    parser.add_argument(
        "--train",
        action="store_true",
        default=True,
        help="Run training pipeline (default)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("🚀 ML DASHBOARD - SETUP AND TRAINING")
    print("=" * 80 + "\n")
    
    if args.config:
        print_config()
        return 0
    
    try:
        # Setup environment
        if not setup_environment():
            return 1
        
        if args.setup_only:
            logger.info("✅ Environment setup completed!")
            return 0
        
        # Run training
        if not run_training():
            return 1
        
        print("\n" + "=" * 80)
        print("✅ SETUP AND TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Start the backend API: python -m uvicorn backend.app.main:app --reload")
        print("2. Start the frontend: cd frontend && npm start")
        print("3. Access the dashboard at: http://localhost:4200")
        print("4. View MLflow UI: http://localhost:5000")
        print("=" * 80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Setup interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
