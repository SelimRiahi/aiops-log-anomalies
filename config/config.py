"""
Configuration settings for MLOps Fraud Detection System
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR
LOGS_DIR = BASE_DIR / "logs"

# Model files
AUTOENCODER_PATH = MODEL_DIR / "autoencoder.keras"
ENCODER_PATH = MODEL_DIR / "encoder.keras"
SCALER_PATH = MODEL_DIR / "autoencoder_scaler.pkl"
THRESHOLD_PATH = MODEL_DIR / "ae_threshold.npy"

# Create directories if they don't exist
MODEL_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_WORKERS = int(os.getenv("API_WORKERS", 4))

# Model Configuration
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.95))

# Monitoring Configuration
ENABLE_MONITORING = os.getenv("ENABLE_MONITORING", "true").lower() == "true"
METRICS_RETENTION_DAYS = int(os.getenv("METRICS_RETENTION_DAYS", 30))

# Drift Detection Configuration
DRIFT_CHECK_INTERVAL_HOURS = int(os.getenv("DRIFT_CHECK_INTERVAL_HOURS", 24))
DRIFT_THRESHOLD = float(os.getenv("DRIFT_THRESHOLD", 0.1))

# Retraining Configuration
AUTO_RETRAIN = os.getenv("AUTO_RETRAIN", "true").lower() == "true"
RETRAIN_INTERVAL_DAYS = int(os.getenv("RETRAIN_INTERVAL_DAYS", 7))
MIN_SAMPLES_FOR_RETRAIN = int(os.getenv("MIN_SAMPLES_FOR_RETRAIN", 1000))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
