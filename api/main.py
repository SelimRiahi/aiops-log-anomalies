"""
FastAPI Main Application - Fraud Detection API
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
from datetime import datetime
import sys
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from api.schemas import TransactionRequest, PredictionResponse, HealthResponse, MetricsResponse
from api.model_handler import model_handler
from monitoring.metrics_tracker import metrics_tracker
from config.config import MODEL_VERSION, API_HOST, API_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Fraud Detection API",
    description="MLOps-enabled fraud detection system using Autoencoder",
    version=MODEL_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track API start time
start_time = time.time()


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("=" * 80)
    logger.info("Starting Fraud Detection API")
    logger.info("=" * 80)
    
    success = model_handler.load_model()
    if not success:
        logger.error("Failed to load model! API will not work properly.")
    else:
        logger.info("API ready to serve predictions")
        logger.info(f"Listening on {API_HOST}:{API_PORT}")


@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "service": "Fraud Detection API",
        "version": MODEL_VERSION,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "metrics": "/metrics",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model_handler.is_loaded() else "unhealthy",
        model_loaded=model_handler.is_loaded(),
        model_version=MODEL_VERSION
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_fraud(transaction: TransactionRequest, request: Request):
    """
    Predict if a transaction is fraudulent
    
    - **transaction**: Transaction data with all required fields
    - Returns fraud prediction with confidence score
    """
    start_time_request = time.time()
    
    try:
        # Check if model is loaded
        if not model_handler.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Make prediction
        is_fraud, fraud_prob, reconstruction_error, confidence = model_handler.predict(
            transaction.model_dump()
        )
        
        # Calculate response time
        response_time = (time.time() - start_time_request) * 1000  # ms
        
        # Track metrics
        metrics_tracker.record_prediction(
            is_fraud=is_fraud,
            reconstruction_error=reconstruction_error,
            response_time_ms=response_time,
            transaction_data=transaction.model_dump()
        )
        
        # Log prediction
        logger.info(
            f"Prediction: fraud={is_fraud}, error={reconstruction_error:.4f}, "
            f"confidence={confidence:.2f}, time={response_time:.2f}ms"
        )
        
        return PredictionResponse(
            is_fraud=is_fraud,
            fraud_probability=fraud_prob,
            reconstruction_error=reconstruction_error,
            threshold=float(model_handler.threshold),
            confidence=confidence,
            model_version=MODEL_VERSION
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_test_sample", response_model=PredictionResponse, tags=["Prediction"])
async def predict_test_sample(sample_index: int = 0):
    """
    Predict fraud using a sample from test data (has real user history features)
    
    - **sample_index**: Index of sample from test data (0 to 9997)
    - Returns prediction with actual fraud label for comparison
    
    This endpoint uses pre-computed features with real user history,
    so predictions are more accurate than arbitrary transactions.
    """
    start_time_request = time.time()
    
    try:
        # Check if model is loaded
        if not model_handler.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Load test data
        test_data_path = Path(__file__).parent.parent / 'paysim_test.csv'
        if not test_data_path.exists():
            raise HTTPException(status_code=404, detail="Test data not found")
        
        import pandas as pd
        test_df = pd.read_csv(test_data_path)
        
        if sample_index < 0 or sample_index >= len(test_df):
            raise HTTPException(
                status_code=400, 
                detail=f"Sample index must be between 0 and {len(test_df)-1}"
            )
        
        # Get sample
        sample = test_df.iloc[sample_index]
        actual_fraud = bool(sample['isFraud'])
        
        # Extract features (exclude isFraud label)
        feature_cols = [col for col in test_df.columns if col != 'isFraud']
        features = sample[feature_cols].values.reshape(1, -1)
        
        # Scale features
        features_scaled = model_handler.scaler.transform(features)
        
        # Predict
        reconstructed = model_handler.autoencoder.predict(features_scaled, verbose=0)
        reconstruction_error = float(np.mean(np.abs(reconstructed - features_scaled)))
        
        # Determine fraud
        is_fraud = reconstruction_error > model_handler.threshold
        fraud_prob = min(reconstruction_error / model_handler.threshold, 1.0)
        confidence = abs(fraud_prob - 0.5) * 2
        
        # Calculate response time
        response_time = (time.time() - start_time_request) * 1000
        
        # Track metrics
        metrics_tracker.record_prediction(
            is_fraud=is_fraud,
            reconstruction_error=reconstruction_error,
            response_time_ms=response_time,
            transaction_data={
                'amount': float(sample['amount']),
                'type': 'TEST_SAMPLE'
            }
        )
        
        # Create response with actual label
        response = PredictionResponse(
            is_fraud=is_fraud,
            fraud_probability=fraud_prob,
            reconstruction_error=reconstruction_error,
            threshold=model_handler.threshold,
            confidence=confidence,
            model_version=MODEL_VERSION
        )
        
        # Add actual label to response for comparison
        logger.info(
            f"Test sample {sample_index}: Predicted={is_fraud}, "
            f"Actual={actual_fraud}, Error={reconstruction_error:.4f}"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Test prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics", response_model=MetricsResponse, tags=["Monitoring"])
async def get_metrics():
    """Get API and model metrics"""
    uptime = time.time() - start_time
    stats = metrics_tracker.get_statistics()
    
    return MetricsResponse(
        total_predictions=stats['total_predictions'],
        fraud_detected=stats['fraud_detected'],
        fraud_rate=stats['fraud_rate'],
        avg_response_time_ms=stats['avg_response_time_ms'],
        uptime_seconds=uptime
    )


@app.get("/metrics/detailed", tags=["Monitoring"])
async def get_detailed_metrics():
    """Get detailed metrics including recent predictions"""
    return {
        "statistics": metrics_tracker.get_statistics(),
        "recent_predictions": metrics_tracker.get_recent_predictions(limit=10),
        "uptime_seconds": time.time() - start_time
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
